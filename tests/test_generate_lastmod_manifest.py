import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "scripts"
    / "generate-lastmod-manifest.py"
)

spec = importlib.util.spec_from_file_location(
    "generate_lastmod_manifest", SCRIPT_PATH
)
manifest_script = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manifest_script)


class TestGenerateLastmodManifest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo_root = Path(self._tmp.name)
        (self.repo_root / "templates").mkdir()

        self._run_git("init", "-q")
        self._run_git("config", "user.email", "test@test.com")
        self._run_git("config", "user.name", "Test")

        self._orig_repo_root = manifest_script.REPO_ROOT
        self._orig_manifest_path = manifest_script.MANIFEST_PATH
        manifest_script.REPO_ROOT = str(self.repo_root)
        manifest_script.MANIFEST_PATH = str(
            self.repo_root / manifest_script.MANIFEST_REL_PATH
        )

    def tearDown(self):
        manifest_script.REPO_ROOT = self._orig_repo_root
        manifest_script.MANIFEST_PATH = self._orig_manifest_path
        self._tmp.cleanup()

    def _run_git(self, *args):
        subprocess.run(
            ["git", *args], cwd=self.repo_root, check=True, capture_output=True
        )

    def _commit(self, message, date, paths=None):
        self._run_git("add", *(paths or ["-A"]))
        subprocess.run(
            ["git", "commit", "-q", "-m", message],
            cwd=self.repo_root,
            check=True,
            capture_output=True,
            env={
                **os.environ,
                "GIT_AUTHOR_DATE": date,
                "GIT_COMMITTER_DATE": date,
            },
        )

    def _write(self, rel_path, content):
        path = self.repo_root / "templates" / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def _read_manifest(self):
        with open(manifest_script.MANIFEST_PATH) as f:
            return json.load(f)

    def test_full_rebuild_walks_all_history(self):
        self._write("a.html", "a")
        self._commit("add a", "2020-01-01T00:00:00")

        manifest_script._generate()

        self.assertEqual(self._read_manifest(), {"a.html": "2020-01-01"})

    def test_incremental_update_preserves_untouched_and_updates_changed(self):
        self._write("a.html", "a")
        self._commit("add a", "2020-01-01T00:00:00")
        manifest_script._generate()
        self._commit("commit manifest v1", "2020-01-02T00:00:00")

        self._write("a.html", "a2")
        self._write("b.html", "b")
        self._commit("update a, add b", "2020-06-01T00:00:00")

        manifest_script._generate()

        self.assertEqual(
            self._read_manifest(),
            {"a.html": "2020-06-01", "b.html": "2020-06-01"},
        )

    def test_incremental_ignores_commits_outside_templates(self):
        self._write("a.html", "a")
        self._commit("add a", "2020-01-01T00:00:00")
        manifest_script._generate()
        self._commit("commit manifest v1", "2020-01-02T00:00:00")

        (self.repo_root / "README.md").write_text("unrelated")
        self._commit("unrelated change", "2020-07-01T00:00:00")

        manifest_script._generate()

        self.assertEqual(self._read_manifest(), {"a.html": "2020-01-01"})

    def test_falls_back_to_full_rebuild_when_manifest_untracked(self):
        self._write("a.html", "a")
        self._commit("add a", "2020-01-01T00:00:00")
        # First _generate() call writes the manifest but nothing commits
        # it -- it stays untracked, same as it being gitignored.
        manifest_script._generate()

        self._write("b.html", "b")
        # Stage only b.html: the manifest from the untracked _generate()
        # call above must stay untracked, same as it being gitignored.
        self._commit(
            "add b", "2020-02-01T00:00:00", paths=["templates/b.html"]
        )

        manifest_script._generate()

        self.assertEqual(
            self._read_manifest(),
            {"a.html": "2020-01-01", "b.html": "2020-02-01"},
        )

    def test_falls_back_to_full_rebuild_on_corrupt_manifest(self):
        self._write("a.html", "a")
        self._commit("add a", "2020-01-01T00:00:00")
        manifest_script._generate()
        self._commit("commit manifest v1", "2020-01-02T00:00:00")

        Path(manifest_script.MANIFEST_PATH).write_text("not valid json {{{")

        manifest_script._generate()

        self.assertEqual(self._read_manifest(), {"a.html": "2020-01-01"})

    def test_manifest_does_not_list_itself(self):
        self._write("a.html", "a")
        self._commit("add a", "2020-01-01T00:00:00")
        manifest_script._generate()
        self._commit("commit manifest v1", "2020-01-02T00:00:00")

        # A second incremental run walks the commit that added the
        # manifest itself under templates/; it must not appear as an
        # entry of itself.
        manifest_script._generate()

        self.assertNotIn(
            manifest_script.MANIFEST_BASENAME, self._read_manifest()
        )


if __name__ == "__main__":
    unittest.main()
