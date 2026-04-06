"""Split normalized source materials into structured episode chunks."""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from utils import ensure_dir, iter_files, normalize_text, repo_root, write_json


FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MAIN_BODY_DATE_PATTERNS = (
    re.compile(r"大家好[，,\s]+(\d{4})年(\d{1,2})月(\d{1,2})日"),
    re.compile(r"睡前消息[:：]?\s*(\d{2})/(\d{1,2})/(\d{1,2})"),
    re.compile(r"睡前消息\s*(20\d{2})(\d{2})(\d{2})"),
)
LIVESTREAM_TITLE_DATE_RE = re.compile(r"【(\d{4})年(\d{1,2})月(\d{1,2})日】")
KBD_RE = re.compile(r"<k?bd>(.*?)</k?bd>", re.IGNORECASE)
MAIN_PROMPT_RE = re.compile(
    r"<font color=\"indigo\">(.*?)</font>", re.DOTALL | re.IGNORECASE
)
LIVESTREAM_BLOCK_RE = re.compile(
    r"(?ms)^>\s*(.+?)\n\n(.*?)(?=^>\s|\n---\n|\Z)"
)
SENTENCE_SPLIT_RE = re.compile(r"[。！？!?]\s*")
DATE_SEARCH_NOISE_RE = re.compile(
    r"# Tabs \{\.tabset\}.*?\n#\n|<iframe.*?</iframe>|<div.*?>|</div>",
    re.DOTALL | re.IGNORECASE,
)


@dataclass
class Episode:
    """A normalized episode page ready for chunking."""

    source_type: str
    relative_path: Path
    title: str
    date: str
    date_source: str
    body: str
    description: str
    episode_id: str


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Split normalized archive files into chunked episode directories."
    )
    parser.add_argument(
        "--input-root",
        default=str(repo_root() / "data" / "normalized"),
        help="Normalized archive root.",
    )
    parser.add_argument(
        "--output-root",
        default=str(repo_root() / "data" / "chunked"),
        help="Chunked output directory.",
    )
    return parser.parse_args()


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Parse a simple YAML-like front matter block."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text

    front_matter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front_matter[key.strip()] = value.strip()
    body = text[match.end() :].lstrip("\n")
    return front_matter, body


def slug_from_path(source_type: str, relative_path: Path) -> str:
    """Build a stable ASCII episode id from the source path."""
    parts = [source_type, *relative_path.with_suffix("").parts]
    return "-".join(part.replace(" ", "-") for part in parts)


def detect_index_page(source_type: str, relative_path: Path, title: str, body: str) -> bool:
    """Return whether a file is a navigation/index page instead of content."""
    if source_type == "main":
        if re.fullmatch(r"第\d+-\d+期", title):
            return True
        if "{.links-list}" in body and "](/main/" in body:
            return True
    if source_type == "livestream":
        if re.fullmatch(r"\d{4}年", title) and "links-list" in body:
            return True
        if relative_path.name.endswith(".md") and "## Tabs {.tabset}" in body and "](./" in body:
            return True
    return False


def extract_main_date(title: str, body: str, fallback: str) -> tuple[str, str]:
    """Extract the actual main episode date when possible."""
    date_search_body = DATE_SEARCH_NOISE_RE.sub("\n", body)
    for pattern in MAIN_BODY_DATE_PATTERNS:
        match = pattern.search(date_search_body[:12000])
        if not match:
            continue
        year, month, day = match.groups()
        normalized_year = int(year)
        if len(year) == 2:
            normalized_year += 2000
        return (
            f"{normalized_year:04d}-{int(month):02d}-{int(day):02d}",
            "body_explicit",
        )
    if fallback:
        return fallback[:10], "front_matter_fallback"
    return "unknown", "unknown"


def extract_livestream_date(title: str, fallback: str) -> tuple[str, str]:
    """Extract livestream date from title when possible."""
    match = LIVESTREAM_TITLE_DATE_RE.search(title)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}", "title_explicit"
    if fallback:
        return fallback[:10], "front_matter_fallback"
    return "unknown", "unknown"


def build_episode(source_type: str, root: Path, path: Path) -> Episode | None:
    """Convert a normalized file into an Episode object, or None if skipped."""
    relative_path = path.relative_to(root / source_type)
    raw_text = path.read_text(encoding="utf-8")
    front_matter, body = parse_front_matter(raw_text)
    title = front_matter.get("title", path.stem)
    description = clean_description(front_matter.get("description", ""))

    if detect_index_page(source_type, relative_path, title, body):
        return None

    if source_type == "main":
        date, date_source = extract_main_date(title, body, front_matter.get("date", ""))
    else:
        date, date_source = extract_livestream_date(title, front_matter.get("date", ""))

    return Episode(
        source_type=source_type,
        relative_path=relative_path,
        title=title,
        date=date,
        date_source=date_source,
        body=body,
        description=description,
        episode_id=slug_from_path(source_type, relative_path),
    )


def clean_description(description: str) -> str:
    """Clean malformed or overly noisy description text from source front matter."""
    cleaned = description.strip()
    if "', 'dynamic': '" in cleaned:
        cleaned = cleaned.split("', 'dynamic': '", 1)[0].strip()
    cleaned = cleaned.strip("'\" ")
    return cleaned


def split_main_episode(episode: Episode) -> list[dict[str, object]]:
    """Split a main episode by presenter question prompts."""
    body = episode.body
    matches = list(MAIN_PROMPT_RE.finditer(body))
    chunks: list[dict[str, object]] = []

    if not matches:
        cleaned = cleanup_chunk_text(body)
        if cleaned:
            chunks.append(
                {
                    "heading": episode.title,
                    "question": "",
                    "content": cleaned,
                }
            )
        return chunks

    for index, match in enumerate(matches, start=1):
        question = cleanup_inline_text(match.group(1))
        start = match.end()
        end = matches[index].start() if index < len(matches) else len(body)
        content = cleanup_chunk_text(body[start:end])
        if not content:
            continue
        heading, normalized_question = normalize_heading(
            question, content, f"{episode.title} - {index}"
        )
        chunks.append(
            {
                "heading": heading,
                "question": normalized_question,
                "content": content,
            }
        )
    return chunks


def split_livestream_episode(episode: Episode) -> list[dict[str, object]]:
    """Split a livestream page by quoted question headings."""
    body = episode.body
    chunks: list[dict[str, object]] = []

    for match in LIVESTREAM_BLOCK_RE.finditer(body):
        question = cleanup_inline_text(match.group(1))
        content = cleanup_chunk_text(match.group(2))
        if not content:
            continue
        heading, normalized_question = normalize_heading(question, content, episode.title)
        chunks.append(
            {
                "heading": heading,
                "question": normalized_question,
                "content": content,
            }
        )

    if chunks:
        return chunks

    cleaned = cleanup_chunk_text(body)
    if cleaned:
        chunks.append(
            {
                "heading": episode.title,
                "question": "",
                "content": cleaned,
            }
        )
    return chunks


def extract_episode_keywords(episode: Episode) -> list[str]:
    """Extract lightweight episode keywords from title/body."""
    keywords: list[str] = []
    for raw in KBD_RE.findall(episode.body):
        keyword = cleanup_inline_text(raw)
        if keyword and keyword not in keywords:
            keywords.append(keyword)
    return keywords[:12]


def cleanup_inline_text(text: str) -> str:
    """Clean a short line of inline markdown/html noise."""
    cleaned = text
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = cleaned.replace("&nbsp;", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" -\t\n\r")


def cleanup_chunk_text(text: str) -> str:
    """Conservatively clean chunk content while keeping source meaning."""
    cleaned = text
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", cleaned)
    cleaned = re.sub(r"<iframe.*?</iframe>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<div.*?>|</div>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<font[^>]*>|</font>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<u>|</u>|<kbd>|</kbd>|<Kbd>|</Kbd>", "", cleaned)
    cleaned = re.sub(r"\*\*遵循著作人.*", "", cleaned)
    cleaned = re.sub(r"^# Tabs \{\.tabset\}\n.*?(?=\n#\n|\n> |\n-\s-\s-\n|\n---\n|\Z)", "", cleaned, flags=re.DOTALL | re.MULTILINE)
    cleaned = re.sub(r"^##\s.*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^<http[^>]+>$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^https?://\S+$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    stripped = cleaned.strip()
    if not stripped:
        return ""
    if not re.search(r"[\u4e00-\u9fffA-Za-z0-9]", stripped):
        return ""
    return normalize_text(cleaned)


def normalize_heading(question: str, content: str, fallback: str) -> tuple[str, str]:
    """Repair weak or truncated headings using the content when necessary."""
    heading = question.strip() if question else ""
    if not heading:
        return fallback, ""

    weak_heading = False
    if len(heading) <= 3:
        weak_heading = True
    if re.match(r"^[\u4e00-\u9fffA-Za-z0-9]{0,1}问题", heading):
        weak_heading = True
    if heading.startswith("口问题"):
        weak_heading = True
    if heading in {"问题", "怎么看", "如何看待"}:
        weak_heading = True

    if not weak_heading:
        return heading, heading

    body = re.sub(r"\s+", " ", content).strip()
    if not body:
        return fallback, ""
    first_sentence = SENTENCE_SPLIT_RE.split(body, maxsplit=1)[0].strip()
    if not first_sentence:
        return fallback, ""
    repaired = first_sentence[:36]
    return repaired, repaired


def write_episode_output(output_root: Path, episode: Episode, chunks: list[dict[str, object]]) -> None:
    """Write an episode directory with meta and chunk markdown files."""
    episode_dir = ensure_dir(output_root / episode.source_type / episode.episode_id)
    for stale_chunk in episode_dir.glob("chunk-*.md"):
        stale_chunk.unlink()
    keywords = extract_episode_keywords(episode)

    meta_lines = [
        f"# {episode.title}",
        "",
        f"- `episode_id`: {episode.episode_id}",
        f"- `source_type`: {episode.source_type}",
        f"- `date`: {episode.date}",
        f"- `date_source`: {episode.date_source}",
        f"- `source_path`: {episode.relative_path.as_posix()}",
    ]
    if episode.description:
        meta_lines.append(f"- `description`: {episode.description}")
    if keywords:
        meta_lines.append(f"- `keywords`: {', '.join(keywords)}")

    meta_lines.extend(["", "## Chunks", ""])

    chunk_manifest: list[dict[str, object]] = []

    for index, chunk in enumerate(chunks, start=1):
        chunk_name = f"chunk-{index:03d}.md"
        chunk_path = episode_dir / chunk_name
        chunk_manifest.append(
            {
                "chunk_file": chunk_name,
                "chunk_index": index,
                "heading": chunk["heading"],
                "question": chunk["question"],
            }
        )
        meta_lines.append(f"- `{chunk_name}`: {chunk['heading']}")

        chunk_lines = [
            "---",
            f"title: {episode.title}",
            f"date: {episode.date}",
            f"date_source: {episode.date_source}",
            f"source_type: {episode.source_type}",
            f"episode_id: {episode.episode_id}",
            f"chunk_index: {index}",
            f"chunk_heading: {chunk['heading']}",
            f"source_path: {episode.relative_path.as_posix()}",
            "---",
            "",
            f"# {chunk['heading']}",
        ]
        if chunk["question"]:
            chunk_lines.extend(["", f"## 提问", "", chunk["question"]])
        chunk_lines.extend(["", "## 内容", "", chunk["content"].rstrip(), ""])
        chunk_path.write_text("\n".join(chunk_lines), encoding="utf-8")

    (episode_dir / "meta.md").write_text("\n".join(meta_lines) + "\n", encoding="utf-8")
    write_json(
        episode_dir / "meta.json",
        {
            "episode_id": episode.episode_id,
            "source_type": episode.source_type,
            "title": episode.title,
            "date": episode.date,
            "date_source": episode.date_source,
            "description": episode.description,
            "source_path": episode.relative_path.as_posix(),
            "keywords": keywords,
            "chunk_count": len(chunk_manifest),
            "chunks": chunk_manifest,
        },
    )


def process_source_type(input_root: Path, output_root: Path, source_type: str) -> dict[str, int]:
    """Process one source type and return summary stats."""
    source_dir = input_root / source_type
    target_dir = output_root / source_type
    stats = {
        "source_files": 0,
        "skipped_index_pages": 0,
        "skipped_empty_pages": 0,
        "episodes_written": 0,
        "chunks_written": 0,
    }
    if not source_dir.exists():
        return stats
    if target_dir.exists():
        shutil.rmtree(target_dir)
    ensure_dir(target_dir)

    for path in iter_files(source_dir):
        if path.suffix.lower() != ".md":
            continue
        stats["source_files"] += 1
        episode = build_episode(source_type, input_root, path)
        if episode is None:
            stats["skipped_index_pages"] += 1
            continue

        chunks = (
            split_main_episode(episode)
            if source_type == "main"
            else split_livestream_episode(episode)
        )
        if not chunks:
            stats["skipped_empty_pages"] += 1
            continue

        write_episode_output(output_root, episode, chunks)
        stats["episodes_written"] += 1
        stats["chunks_written"] += len(chunks)

    return stats


def main() -> None:
    """Split normalized source materials into chunked episode directories."""
    args = parse_args()
    input_root = Path(args.input_root).resolve()
    output_root = Path(args.output_root).resolve()

    if not input_root.exists():
        raise FileNotFoundError(
            f"Input root not found: {input_root}. Run normalize_archive.py first."
        )

    ensure_dir(output_root)
    summary: dict[str, object] = {
        "input_root": str(input_root),
        "output_root": str(output_root),
        "stats": {},
    }

    for source_type in ("main", "livestream"):
        summary["stats"][source_type] = process_source_type(input_root, output_root, source_type)

    write_json(output_root / "manifest.json", summary)

    print(f"Chunked output written to: {output_root}")
    for source_type, stats in summary["stats"].items():
        print(
            f"{source_type}: "
            f"{stats['episodes_written']} episodes, "
            f"{stats['chunks_written']} chunks, "
            f"{stats['skipped_index_pages']} skipped index pages, "
            f"{stats['skipped_empty_pages']} skipped empty pages"
        )


if __name__ == "__main__":
    main()
