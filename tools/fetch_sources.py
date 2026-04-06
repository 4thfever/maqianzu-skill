"""Fetch upstream source materials for the Ma Qianzu skill knowledge base."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from utils import ensure_dir, repo_root


DEFAULT_REPO_URL = "https://github.com/bedtimenews/bedtimenews-archive-contents.git"
ALLOWED_PATHS = ("main", "livestream")


def run_git(args: list[str], cwd: Path | None = None) -> None:
    """Run git and raise a readable error on failure."""
    subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        check=True,
    )


def current_remote(path: Path) -> str | None:
    """Return the configured origin URL if available."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(path),
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return None
    return result.stdout.strip() or None


def clone_sparse(repo_url: str, destination: Path) -> None:
    """Clone the upstream repository using sparse checkout."""
    run_git(
        [
            "clone",
            "--depth",
            "1",
            "--filter=blob:none",
            "--sparse",
            repo_url,
            str(destination),
        ]
    )
    run_git(["sparse-checkout", "set", *ALLOWED_PATHS], cwd=destination)


def update_sparse_checkout(destination: Path) -> None:
    """Update an existing sparse checkout."""
    run_git(["sparse-checkout", "set", *ALLOWED_PATHS], cwd=destination)
    run_git(["pull", "--ff-only"], cwd=destination)


def count_files(path: Path) -> int:
    """Count files recursively under a directory if it exists."""
    if not path.exists():
        return 0
    return sum(1 for candidate in path.rglob("*") if candidate.is_file())


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch only main and livestream from bedtimenews archive."
    )
    parser.add_argument(
        "--repo-url",
        default=DEFAULT_REPO_URL,
        help="Upstream Git repository URL.",
    )
    parser.add_argument(
        "--destination",
        default=str(repo_root() / "data" / "upstream" / "bedtimenews-archive-contents"),
        help="Local sparse checkout path.",
    )
    return parser.parse_args()


def main() -> None:
    """Fetch or update the upstream sparse checkout."""
    args = parse_args()
    destination = Path(args.destination).resolve()
    ensure_dir(destination.parent)

    if not destination.exists():
        clone_sparse(args.repo_url, destination)
    else:
        remote = current_remote(destination)
        if remote != args.repo_url:
            raise RuntimeError(
                f"Existing directory {destination} does not match repo {args.repo_url}."
            )
        update_sparse_checkout(destination)

    main_count = count_files(destination / "main")
    livestream_count = count_files(destination / "livestream")
    print(f"Fetched source repo to: {destination}")
    print(f"Included paths: {', '.join(ALLOWED_PATHS)}")
    print(f"main files: {main_count}")
    print(f"livestream files: {livestream_count}")


if __name__ == "__main__":
    main()
