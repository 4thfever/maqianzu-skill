"""Safety regression tests for destructive knowledge build operations."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
import unittest


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from fetch_sources import require_standalone_checkout  # noqa: E402
import build_all  # noqa: E402
from utils import prepare_output_dir, require_distinct_trees  # noqa: E402


class BuildSafetyTests(unittest.TestCase):
    def test_nonempty_output_requires_replace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                prepare_output_dir(output, replace=False)

            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_replace_removes_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            output.mkdir()
            (output / "old.txt").write_text("old", encoding="utf-8")

            prepare_output_dir(output, replace=True)

            self.assertTrue(output.is_dir())
            self.assertEqual(list(output.iterdir()), [])

    def test_overlapping_trees_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(ValueError):
                require_distinct_trees(root, root / "child")
            with self.assertRaises(ValueError):
                require_distinct_trees(root / "child", root)

    def test_parent_git_repository_is_not_accepted_as_source_checkout(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        inherited_directory = repository / "tmp" / "not-a-checkout"
        inherited_directory.mkdir(parents=True, exist_ok=True)
        self.addCleanup(lambda: inherited_directory.rmdir())

        with self.assertRaises(RuntimeError):
            require_standalone_checkout(
                inherited_directory,
                "https://github.com/bedtimenews/bedtimenews-archive-contents.git",
            )

    def test_backup_restore_recovers_outputs_and_removes_new_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original_root = build_all.ROOT
            original_paths = build_all.PROTECTED_PATHS
            build_all.ROOT = root
            build_all.PROTECTED_PATHS = (Path("existing"), Path("created-during-build"))
            self.addCleanup(setattr, build_all, "ROOT", original_root)
            self.addCleanup(setattr, build_all, "PROTECTED_PATHS", original_paths)

            existing = root / "existing"
            existing.mkdir()
            (existing / "value.txt").write_text("before", encoding="utf-8")
            backup_root, copied = build_all.backup_outputs()

            (existing / "value.txt").write_text("after", encoding="utf-8")
            created = root / "created-during-build"
            created.mkdir()
            (created / "new.txt").write_text("new", encoding="utf-8")
            build_all.restore_outputs(backup_root, copied)

            self.assertEqual(
                (existing / "value.txt").read_text(encoding="utf-8"), "before"
            )
            self.assertFalse(created.exists())


if __name__ == "__main__":
    unittest.main()
