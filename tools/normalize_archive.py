"""Normalize upstream archive files into a stable local format."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil

from utils import (
    ensure_dir,
    is_text_file,
    iter_files,
    normalize_text,
    read_text_with_fallbacks,
    repo_root,
    write_json,
)


ALLOWED_PATHS = ("main", "livestream")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Normalize main and livestream source files into a build directory."
    )
    parser.add_argument(
        "--source-root",
        default=str(repo_root() / "data" / "upstream" / "bedtimenews-archive-contents"),
        help="Sparse checkout root produced by fetch_sources.py.",
    )
    parser.add_argument(
        "--output-root",
        default=str(repo_root() / "data" / "normalized"),
        help="Normalized output directory.",
    )
    return parser.parse_args()


def normalize_tree(source_root: Path, output_root: Path) -> dict[str, object]:
    """Normalize the allowed source trees and return a manifest payload."""
    if output_root.exists():
        shutil.rmtree(output_root)
    ensure_dir(output_root)
    manifest: dict[str, object] = {
        "source_root": str(source_root),
        "output_root": str(output_root),
        "allowed_paths": list(ALLOWED_PATHS),
        "stats": {},
    }

    for source_type in ALLOWED_PATHS:
        source_dir = source_root / source_type
        target_dir = ensure_dir(output_root / source_type)
        stats = {
            "source_type": source_type,
            "source_files": 0,
            "normalized_files": 0,
            "skipped_non_text": 0,
            "encodings": {},
        }

        if not source_dir.exists():
            manifest["stats"][source_type] = stats
            continue

        for source_file in iter_files(source_dir):
            stats["source_files"] += 1
            if not is_text_file(source_file):
                stats["skipped_non_text"] += 1
                continue

            relative_path = source_file.relative_to(source_dir)
            destination = target_dir / relative_path
            ensure_dir(destination.parent)

            text, encoding = read_text_with_fallbacks(source_file)
            destination.write_text(normalize_text(text), encoding="utf-8")

            stats["normalized_files"] += 1
            stats["encodings"][encoding] = stats["encodings"].get(encoding, 0) + 1

        manifest["stats"][source_type] = stats

    return manifest


def main() -> None:
    """Normalize fetched archive sources and write a manifest."""
    args = parse_args()
    source_root = Path(args.source_root).resolve()
    output_root = Path(args.output_root).resolve()

    if not source_root.exists():
        raise FileNotFoundError(
            f"Source root not found: {source_root}. Run fetch_sources.py first."
        )

    manifest = normalize_tree(source_root, output_root)
    write_json(output_root / "manifest.json", manifest)

    print(f"Normalized archive written to: {output_root}")
    for source_type, stats in manifest["stats"].items():
        print(
            f"{source_type}: "
            f"{stats['normalized_files']} text files, "
            f"{stats['skipped_non_text']} skipped non-text files"
        )


if __name__ == "__main__":
    main()
