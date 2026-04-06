"""Run the full local knowledge build pipeline in the correct order."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STEPS = [
    ("fetch sources", [sys.executable, "tools/fetch_sources.py"]),
    ("normalize archive", [sys.executable, "tools/normalize_archive.py"]),
    ("split chunks", [sys.executable, "tools/split_chunks.py"]),
    ("build indexes", [sys.executable, "tools/build_index.py"]),
    ("validate knowledge", [sys.executable, "tools/validate_knowledge.py"]),
]


def main() -> None:
    """Run the full pipeline and stop on first failure."""
    for label, command in STEPS:
        print(f"==> {label}")
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
