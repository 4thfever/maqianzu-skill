"""Build knowledge indexes from chunked episode outputs."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from dataclasses import dataclass
from pathlib import Path
import re
import shutil
from typing import Iterable

from utils import ensure_dir, iter_files, repo_root, write_json


TOPIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "economy": (
        "经济",
        "财政",
        "房价",
        "房地产",
        "收入",
        "消费",
        "就业",
        "货币",
        "投资",
        "债",
        "税",
        "企业",
        "市场",
        "通胀",
        "增长",
        "金融",
    ),
    "industry": (
        "工业",
        "产业",
        "制造",
        "工厂",
        "技术",
        "芯片",
        "核电",
        "铁路",
        "高铁",
        "能源",
        "电站",
        "汽车",
        "供应链",
        "化工",
        "电池",
        "工程",
        "基础设施",
    ),
    "governance": (
        "政策",
        "政府",
        "治理",
        "制度",
        "行政",
        "地方",
        "改革",
        "教育局",
        "招生",
        "法院",
        "官员",
        "执法",
        "国企",
        "公共卫生",
        "专项",
        "文件",
    ),
    "society": (
        "教育",
        "医疗",
        "人口",
        "养老",
        "城市",
        "学校",
        "医院",
        "婚姻",
        "生育",
        "住房",
        "社区",
        "村医",
        "高考",
        "大学",
        "学生",
        "社会",
        "农村",
    ),
    "international": (
        "美国",
        "日本",
        "俄罗斯",
        "乌克兰",
        "欧洲",
        "加拿大",
        "沙特",
        "泰国",
        "老挝",
        "中亚",
        "国际",
        "外国",
        "全球",
        "越南",
        "哈萨克斯坦",
        "耶鲁",
        "巴黎",
    ),
    "media": (
        "媒体",
        "自媒体",
        "直播",
        "电影",
        "偶像",
        "舆论",
        "平台",
        "主播",
        "节目",
        "流量",
        "微博",
        "B站",
        "视频",
        "票房",
        "影评",
        "娱乐",
    ),
}

TOPIC_LABELS = {
    "economy": "经济与财政",
    "industry": "工业与产业",
    "governance": "治理与政策执行",
    "society": "社会议题",
    "international": "国际与地缘",
    "media": "媒体与传播",
}

TOPIC_QUESTION_MAP = {
    "economy": "财政、增长、消费、收入分配、房地产、金融",
    "industry": "制造业、产业升级、技术路线、基础设施、能源",
    "governance": "政策执行、地方治理、制度安排、行政激励",
    "society": "教育、医疗、人口、城市、养老、日常社会结构",
    "international": "国际关系、全球产业链、海外案例、地缘竞争",
    "media": "自媒体、舆论、平台传播、影视娱乐、节目本身",
}


@dataclass
class EpisodeRecord:
    """Episode metadata enriched with topic classification."""

    episode_id: str
    source_type: str
    title: str
    date: str
    date_source: str
    description: str
    source_path: str
    keywords: list[str]
    chunk_count: int
    chunk_headings: list[str]
    chunk_samples: list[str]
    relative_meta_path: str
    relative_meta_json_path: str
    topics: list[str]
    topic_scores: dict[str, int]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Build markdown and JSON indexes for the Ma Qianzu knowledge base."
    )
    parser.add_argument(
        "--chunked-root",
        default=str(repo_root() / "data" / "chunked"),
        help="Chunked episode root.",
    )
    parser.add_argument(
        "--knowledge-root",
        default=str(repo_root() / "knowledge"),
        help="Knowledge index output directory.",
    )
    parser.add_argument(
        "--episodes-dirname",
        default="episodes",
        help="Directory under knowledge/ used for published episode files.",
    )
    return parser.parse_args()


def load_episode_records(chunked_root: Path, published_root: Path) -> list[EpisodeRecord]:
    """Load episode metadata from chunked outputs and classify topics."""
    records: list[EpisodeRecord] = []
    for meta_json in iter_files(chunked_root):
        if meta_json.name != "meta.json":
            continue
        payload = json.loads(meta_json.read_text(encoding="utf-8"))
        chunk_headings = [chunk["heading"] for chunk in payload.get("chunks", [])]
        chunk_samples = load_chunk_samples(meta_json.parent)
        topics, scores = classify_topics(
            payload.get("title", ""),
            payload.get("description", ""),
            payload.get("keywords", []),
            chunk_headings,
            chunk_samples,
        )
        records.append(
            EpisodeRecord(
                episode_id=payload["episode_id"],
                source_type=payload["source_type"],
                title=payload["title"],
                date=payload["date"],
                date_source=payload.get("date_source", "unknown"),
                description=payload.get("description", ""),
                source_path=payload["source_path"],
                keywords=list(payload.get("keywords", [])),
                chunk_count=int(payload.get("chunk_count", 0)),
                chunk_headings=chunk_headings,
                chunk_samples=chunk_samples,
                relative_meta_path=(published_root / payload["source_type"] / payload["episode_id"] / "meta.md").relative_to(repo_root()).as_posix(),
                relative_meta_json_path=(published_root / payload["source_type"] / payload["episode_id"] / "meta.json").relative_to(repo_root()).as_posix(),
                topics=topics,
                topic_scores=scores,
            )
        )
    records.sort(key=lambda record: (record.date, record.episode_id), reverse=True)
    return records


def classify_topics(
    title: str,
    description: str,
    keywords: Iterable[str],
    chunk_headings: Iterable[str],
    chunk_samples: Iterable[str],
) -> tuple[list[str], dict[str, int]]:
    """Assign one or more coarse topics using simple keyword matching."""
    combined_text = " ".join(
        [title, description, *keywords, *chunk_headings, *chunk_samples]
    ).lower()
    scores: dict[str, int] = {}
    for topic, topic_keywords in TOPIC_KEYWORDS.items():
        score = sum(combined_text.count(keyword.lower()) for keyword in topic_keywords)
        scores[topic] = score

    max_score = max(scores.values()) if scores else 0
    if max_score <= 0:
        return ["society"], scores

    selected = [topic for topic, score in scores.items() if score >= max_score and score > 0]
    if len(selected) == 1:
        secondary = [topic for topic, score in scores.items() if 0 < score >= max_score - 1 and topic not in selected]
        selected.extend(sorted(secondary)[:1])
    return sorted(dict.fromkeys(selected)), scores


def load_chunk_samples(episode_dir: Path) -> list[str]:
    """Read short samples from chunk files for better topic classification."""
    samples: list[str] = []
    for chunk_path in sorted(episode_dir.glob("chunk-*.md"))[:3]:
        text = chunk_path.read_text(encoding="utf-8")
        marker = "## 内容"
        if marker in text:
            body = text.split(marker, 1)[1]
        else:
            body = text
        cleaned = re.sub(r"\s+", " ", body).strip()
        if cleaned:
            samples.append(cleaned[:500])
    return samples


def write_catalog(knowledge_root: Path, records: list[EpisodeRecord]) -> None:
    """Write a machine-readable catalog for validation and downstream scripts."""
    payload = {
        "episode_count": len(records),
        "topic_labels": TOPIC_LABELS,
        "episodes": [
            {
                "episode_id": record.episode_id,
                "source_type": record.source_type,
                "title": record.title,
                "date": record.date,
                "date_source": record.date_source,
                "description": record.description,
                "source_path": record.source_path,
                "keywords": record.keywords,
                "chunk_count": record.chunk_count,
                "topics": record.topics,
                "topic_scores": record.topic_scores,
                "meta_path": record.relative_meta_path,
                "meta_json_path": record.relative_meta_json_path,
            }
            for record in records
        ],
    }
    write_json(knowledge_root / "catalog.json", payload)


def sync_published_episodes(chunked_root: Path, published_root: Path) -> None:
    """Copy chunked episode directories into the published knowledge layer."""
    if published_root.exists():
        shutil.rmtree(published_root)
    ensure_dir(published_root)

    for source_type in ("main", "livestream"):
        source_dir = chunked_root / source_type
        target_dir = ensure_dir(published_root / source_type)
        if not source_dir.exists():
            continue
        for episode_dir in sorted(source_dir.iterdir()):
            if not episode_dir.is_dir():
                continue
            shutil.copytree(episode_dir, target_dir / episode_dir.name)


def short_summary(record: EpisodeRecord) -> str:
    """Build a concise summary line for an episode."""
    if record.description:
        summary = record.description.strip()
    elif record.chunk_headings:
        summary = "；".join(record.chunk_headings[:3])
    else:
        summary = record.title
    return re.sub(r"\s+", " ", summary).strip()


def write_root_index(knowledge_root: Path, records: list[EpisodeRecord]) -> None:
    """Write the knowledge root markdown index."""
    by_source = Counter(record.source_type for record in records)
    by_topic = Counter(topic for record in records for topic in record.topics)

    lines = [
        "# Knowledge Index",
        "",
        "本文件是 OpenClaw 读取马前卒知识库时的总入口。",
        "",
        "建议读取顺序：",
        "",
        "1. 先读 `knowledge/quickstart.md`",
        "2. 再按需回到本文件查看完整主题分布",
        "3. 再读对应 `knowledge/topics/*.md`",
        "4. 最后按需读取 `knowledge/episodes/.../meta.md` 和具体 chunk",
        "",
        "## 知识库概览",
        "",
        f"- `episodes`: {len(records)}",
        f"- `main`: {by_source.get('main', 0)}",
        f"- `livestream`: {by_source.get('livestream', 0)}",
        "",
        "## 主题入口",
        "",
    ]

    for topic in TOPIC_LABELS:
        lines.append(
            f"- `{topic}` / {TOPIC_LABELS[topic]}：{by_topic.get(topic, 0)} 条相关节目，见 `knowledge/topics/{topic}.md`"
        )

    lines.extend(
        [
            "",
            "## 常见问题到主题的映射",
            "",
        ]
    )
    for topic, prompt in TOPIC_QUESTION_MAP.items():
        lines.append(f"- `{topic}`：{prompt}")

    latest_records = records[:12]
    lines.extend(["", "## 最近节目", ""])
    for record in latest_records:
        lines.append(
            f"- `{record.date}` `{record.source_type}` `{record.episode_id}`：{record.title}"
        )
        lines.append(f"  读取：`{record.relative_meta_path}`")

    (knowledge_root / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def topic_sort_key(record: EpisodeRecord, topic: str) -> tuple[int, str, str]:
    """Sort by topic score then date descending."""
    return (record.topic_scores.get(topic, 0), record.date, record.episode_id)


def write_topic_indexes(knowledge_root: Path, records: list[EpisodeRecord]) -> None:
    """Write topic markdown indexes."""
    topic_dir = ensure_dir(knowledge_root / "topics")
    topic_map: dict[str, list[EpisodeRecord]] = defaultdict(list)
    for record in records:
        for topic in record.topics:
            topic_map[topic].append(record)

    for topic in TOPIC_LABELS:
        topic_records = sorted(
            topic_map.get(topic, []),
            key=lambda record: topic_sort_key(record, topic),
            reverse=True,
        )
        lines = [
            f"# {TOPIC_LABELS[topic]}",
            "",
            f"- `topic`: {topic}",
            f"- `episodes`: {len(topic_records)}",
            f"- `question_scope`: {TOPIC_QUESTION_MAP[topic]}",
            "",
            "## 使用建议",
            "",
            "- 先看本主题页，确认相关节目范围。",
            "- 再按节目条目读取对应 `meta.md`。",
            "- 只有在需要具体论证细节时，再进入 chunk 文件。",
            "",
            "## 推荐优先读取",
            "",
        ]

        for record in topic_records[:25]:
            lines.append(
                f"- `{record.date}` `{record.source_type}` `{record.episode_id}`：{record.title}"
            )
            lines.append(f"  - `meta`: `{record.relative_meta_path}`")
            lines.append(f"  - `summary`: {short_summary(record)}")
            if record.keywords:
                lines.append(f"  - `keywords`: {', '.join(record.keywords[:8])}")

        lines.extend(["", "## 常见分析抓手", ""])
        if topic == "economy":
            lines.extend(
                [
                    "- 看财政、资源、债务和收入分配结构。",
                    "- 追问成本由谁承担、风险由谁兜底。",
                    "- 分清短期刺激和长期可持续性。",
                ]
            )
        elif topic == "industry":
            lines.extend(
                [
                    "- 看产业链位置、技术路线与组织能力。",
                    "- 追问规模化复制的条件是否成立。",
                    "- 分清宣传口号和真实制造能力。",
                ]
            )
        elif topic == "governance":
            lines.extend(
                [
                    "- 看政策目标、执行链条和地方激励是否一致。",
                    "- 追问制度设计为什么会反复产生同类问题。",
                    "- 分清形式公平和实际执行结果。",
                ]
            )
        elif topic == "society":
            lines.extend(
                [
                    "- 看教育、医疗、人口、城市等问题背后的结构约束。",
                    "- 追问普通人会承担什么真实后果。",
                    "- 把情绪性争论重新放回资源配置和制度逻辑中理解。",
                ]
            )
        elif topic == "international":
            lines.extend(
                [
                    "- 用国际或地区对比判断问题是否是孤例。",
                    "- 追问地缘、产业链和组织能力的现实约束。",
                    "- 分清宣传想象和实际国力、资源之间的差距。",
                ]
            )
        elif topic == "media":
            lines.extend(
                [
                    "- 看媒体传播逻辑、平台激励和受众结构。",
                    "- 分清外层传播包装和内层论证框架。",
                    "- 追问节目、平台和流量机制如何塑造内容。",
                ]
            )

        (topic_dir / f"{topic}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """Build markdown and JSON indexes."""
    args = parse_args()
    chunked_root = Path(args.chunked_root).resolve()
    knowledge_root = Path(args.knowledge_root).resolve()
    published_root = knowledge_root / args.episodes_dirname

    if not chunked_root.exists():
        raise FileNotFoundError(
            f"Chunked root not found: {chunked_root}. Run split_chunks.py first."
        )

    ensure_dir(knowledge_root)
    ensure_dir(knowledge_root / "topics")
    for legacy_dir in ("main", "livestream"):
        legacy_path = knowledge_root / legacy_dir
        if legacy_path.exists():
            shutil.rmtree(legacy_path)

    sync_published_episodes(chunked_root, published_root)
    records = load_episode_records(chunked_root, published_root)
    write_catalog(knowledge_root, records)
    write_root_index(knowledge_root, records)
    write_topic_indexes(knowledge_root, records)

    print(f"Knowledge indexes written to: {knowledge_root}")
    print(f"Episodes indexed: {len(records)}")
    for topic in TOPIC_LABELS:
        count = sum(1 for record in records if topic in record.topics)
        print(f"{topic}: {count}")


if __name__ == "__main__":
    main()
