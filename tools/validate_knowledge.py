"""Validate generated knowledge indexes and chunk references."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils import repo_root


TOPICS = ("economy", "industry", "governance", "society", "international", "media")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate the generated knowledge index files."
    )
    parser.add_argument(
        "--knowledge-root",
        default=str(repo_root() / "knowledge"),
        help="Knowledge directory to validate.",
    )
    return parser.parse_args()


def require(path: Path, errors: list[str], label: str) -> None:
    """Record an error if a path does not exist."""
    if not path.exists():
        errors.append(f"Missing {label}: {path}")


def validate_catalog(knowledge_root: Path, errors: list[str]) -> dict[str, object] | None:
    """Load and validate the catalog payload."""
    catalog_path = knowledge_root / "catalog.json"
    require(catalog_path, errors, "catalog")
    if errors:
        return None
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    episodes = payload.get("episodes", [])
    if not isinstance(episodes, list) or not episodes:
        errors.append("catalog.json has no episodes")
        return None
    for episode in episodes:
        meta_path = repo_root() / episode["meta_path"]
        meta_json_path = repo_root() / episode["meta_json_path"]
        require(meta_path, errors, f"episode meta for {episode['episode_id']}")
        require(meta_json_path, errors, f"episode meta.json for {episode['episode_id']}")
        topics = episode.get("topics", [])
        if not topics:
            errors.append(f"Episode {episode['episode_id']} has no topics")
        for topic in topics:
            if topic not in TOPICS:
                errors.append(f"Episode {episode['episode_id']} has unknown topic {topic}")
    return payload


def validate_markdown_indexes(knowledge_root: Path, errors: list[str]) -> None:
    """Validate required markdown index files."""
    require(knowledge_root / "index.md", errors, "root index")
    require(knowledge_root / "episodes", errors, "published episodes directory")
    for topic in TOPICS:
        require(knowledge_root / "topics" / f"{topic}.md", errors, f"topic index {topic}")


def main() -> None:
    """Validate the generated knowledge artifacts."""
    args = parse_args()
    knowledge_root = Path(args.knowledge_root).resolve()
    errors: list[str] = []

    require(knowledge_root, errors, "knowledge root")
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    validate_markdown_indexes(knowledge_root, errors)
    payload = validate_catalog(knowledge_root, errors)

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(f"Knowledge validation passed: {len(payload['episodes'])} episodes indexed.")


if __name__ == "__main__":
    main()
