"""Run the full local knowledge build pipeline in the correct order."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import shutil
import uuid


ROOT = Path(__file__).resolve().parent.parent
FETCH_STEP = ("fetch sources", [sys.executable, "tools/fetch_sources.py"])
BUILD_STEPS = [
    ("normalize archive", [sys.executable, "tools/normalize_archive.py", "--replace"]),
    ("split chunks", [sys.executable, "tools/split_chunks.py", "--replace"]),
    ("build indexes", [sys.executable, "tools/build_index.py", "--replace"]),
    ("validate knowledge", [sys.executable, "tools/validate_knowledge.py"]),
]
PROTECTED_PATHS = (
    Path("data/normalized"),
    Path("data/chunked"),
    Path("knowledge"),
)


def run_step(label: str, command: list[str]) -> None:
    """Run one build step and stop on failure."""
    print(f"==> {label}")
    subprocess.run(command, cwd=ROOT, check=True)


def backup_outputs() -> tuple[Path, list[Path]]:
    """Copy protected outputs before destructive generation begins."""
    backup_root = ROOT / "tmp" / (
        "knowledge-build-backup-"
        + datetime.now().strftime("%Y%m%d-%H%M%S-")
        + uuid.uuid4().hex[:8]
    )
    copied: list[Path] = []
    for relative in PROTECTED_PATHS:
        source = ROOT / relative
        if not source.exists():
            continue
        destination = backup_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)
        copied.append(relative)
    return backup_root, copied


def restore_outputs(backup_root: Path, copied: list[Path]) -> None:
    """Restore protected outputs exactly as they were before the build."""
    for relative in PROTECTED_PATHS:
        current = ROOT / relative
        if current.exists():
            shutil.rmtree(current)
        backup = backup_root / relative
        if relative in copied and backup.exists():
            current.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(backup, current)


def main() -> None:
    """Run the full pipeline with backup and automatic rollback."""
    run_step(*FETCH_STEP)
    backup_root, copied = backup_outputs()
    print(f"Backup created: {backup_root}")
    try:
        for step in BUILD_STEPS:
            run_step(*step)
    except BaseException:
        print("Build failed; restoring protected outputs.", file=sys.stderr)
        restore_outputs(backup_root, copied)
        raise
    else:
        shutil.rmtree(backup_root, ignore_errors=True)
        print("Build completed; temporary backup removed.")


if __name__ == "__main__":
    main()
