"""Build templates/lastmod-manifest.json: script to generate lastmod
   for sitemaps. Runs at build time and uses .git

CLI usage:
    python3 scripts/generate-lastmod-manifest.py generate-lastmod
"""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_PATHSPEC = "templates"
MANIFEST_PATH = os.path.join(
    REPO_ROOT, TEMPLATES_PATHSPEC, "lastmod-manifest.json"
)

# A control character that can't appear in a commit date, so it safely
# marks the start of each git-log record when parsing the output below.
RECORD_MARKER = "\x02"


def build_manifest():
    """
    Walk git history once and record, for every file ever committed
    under templates/, the commit date of the most recent commit that
    touched it.
    """
    result = subprocess.run(
        [
            "git",
            "log",
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

    manifest = {}
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
        # git log is newest-first, so the first commit we see touching
        # a path is its most recent change.
        manifest.setdefault(rel_path, date)

    return manifest


def _generate():
    manifest = build_manifest()
    with open(MANIFEST_PATH, "w") as manifest_file:
        json.dump(manifest, manifest_file, indent=2, sort_keys=True)
        manifest_file.write("\n")
    print(f"generated {MANIFEST_PATH} ({len(manifest)} entries)")
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
