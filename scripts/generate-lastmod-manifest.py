"""Build templates/lastmod-manifest.json: script to generate lastmod
   for sitemaps. Runs at build time and uses .git

Updates incrementally from the manifest's own last commit when one is
committed to the repo, otherwise walks full history.

CLI usage:
    python3 scripts/generate-lastmod-manifest.py generate-lastmod
"""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_PATHSPEC = "templates"
MANIFEST_BASENAME = "lastmod-manifest.json"
MANIFEST_REL_PATH = os.path.join(TEMPLATES_PATHSPEC, MANIFEST_BASENAME)
MANIFEST_PATH = os.path.join(REPO_ROOT, MANIFEST_REL_PATH)

# A control character that can't appear in a commit date, so it safely
# marks the start of each git-log record when parsing the output below.
RECORD_MARKER = "\x02"


def _last_commit_touching(rel_path):
    """SHA of the most recent commit that touched rel_path, or None if
    it has no history (not yet committed, e.g.)."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", rel_path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip() or None


def _changes_since(since_commit):
    """Yield (rel_path, date) for every templates/ path touched by a
    commit after since_commit (or, if None, by any commit ever),
    newest-first."""
    revision_range = f"{since_commit}..HEAD" if since_commit else "HEAD"
    result = subprocess.run(
        [
            "git",
            "log",
            revision_range,
            f"--format={RECORD_MARKER}%cs",
            "--name-only",
            "--",
            TEMPLATES_PATHSPEC,
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    date = None
    for line in result.stdout.splitlines():
        if line.startswith(RECORD_MARKER):
            date = line[len(RECORD_MARKER) :]
            continue

        path = line.strip()
        if not path.startswith(TEMPLATES_PATHSPEC + "/"):
            # --name-only lists every file touched by the commit, not
            # just ones under our pathspec; skip the rest.
            continue

        rel_path = path[len(TEMPLATES_PATHSPEC) + 1 :]
        if rel_path == MANIFEST_BASENAME:
            # The manifest lives under templates/ too, so committing it
            # would otherwise list it as an entry of itself.
            continue

        yield rel_path, date


def build_manifest(base_manifest=None, since_commit=None):
    """
    Record, for every templates/ path touched since since_commit (or
    all of git history, if None), the commit date of the most recent
    commit that touched it -- merged on top of base_manifest, so
    untouched paths keep their prior date.
    """
    manifest = dict(base_manifest or {})
    seen = set()
    for rel_path, date in _changes_since(since_commit):
        if rel_path in seen:
            # git log is newest-first, so the first commit we see
            # touching a path is its most recent change.
            continue
        seen.add(rel_path)
        manifest[rel_path] = date

    return manifest


def _generate():
    # The manifest, once committed, is its own watermark: the commit
    # that last touched it is the point to resume from. No prior
    # commit (first run, or an untracked/gitignored manifest) means a
    # full rebuild.
    since_commit = _last_commit_touching(MANIFEST_REL_PATH)
    base_manifest = {}
    if since_commit:
        try:
            with open(MANIFEST_PATH) as manifest_file:
                base_manifest = json.load(manifest_file)
        except (OSError, json.JSONDecodeError):
            since_commit = None

    manifest = build_manifest(base_manifest, since_commit)
    with open(MANIFEST_PATH, "w") as manifest_file:
        json.dump(manifest, manifest_file, indent=2, sort_keys=True)
        manifest_file.write("\n")

    mode = "incremental" if since_commit else "full"
    print(f"generated {MANIFEST_PATH} ({len(manifest)} entries, {mode})")
    return 0


def main():
    if len(sys.argv) != 2 or sys.argv[1] != "generate-lastmod":
        print(
            "usage: python3 scripts/generate-lastmod-manifest.py "
            "generate-lastmod",
            file=sys.stderr,
        )
        return 1
    return _generate()


if __name__ == "__main__":
    sys.exit(main())
