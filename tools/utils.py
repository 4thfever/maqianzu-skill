"""Shared helpers for Ma Qianzu skill knowledge build scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".text"}
ENCODING_CANDIDATES = ("utf-8", "utf-8-sig", "gb18030", "gbk")


def repo_root() -> Path:
    """Return the repository root based on the current file location."""
    return Path(__file__).resolve().parent.parent


def ensure_dir(path: Path) -> Path:
    """Create a directory if needed and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_text_file(path: Path) -> bool:
    """Return whether the file should be treated as text."""
    return path.suffix.lower() in TEXT_SUFFIXES


def read_text_with_fallbacks(path: Path) -> tuple[str, str]:
    """Read text using a small set of practical Chinese encoding fallbacks."""
    last_error: UnicodeDecodeError | None = None
    for encoding in ENCODING_CANDIDATES:
        try:
            return path.read_text(encoding=encoding), encoding
        except UnicodeDecodeError as exc:
            last_error = exc
    raise UnicodeDecodeError(
        last_error.encoding if last_error else "unknown",
        last_error.object if last_error else b"",
        last_error.start if last_error else 0,
        last_error.end if last_error else 1,
        last_error.reason if last_error else f"Could not decode {path}",
    )


def normalize_text(text: str) -> str:
    """Apply conservative normalization suitable for archive text."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in normalized.split("\n"))
    return normalized.strip() + "\n"


def write_json(path: Path, payload: object) -> None:
    """Write UTF-8 JSON with stable formatting."""
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def iter_files(root: Path) -> Iterable[Path]:
    """Yield files recursively under a root path in sorted order."""
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path
