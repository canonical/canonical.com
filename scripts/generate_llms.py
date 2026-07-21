#!/usr/bin/env python3
"""Pre-generate llms-full.txt at build time.

Renders every renderable page linked from llms.txt (see
webapp.llms.build_llms_full_txt), which is too slow to redo on every app
worker's cold start. Invoked from .github/workflows/deploy.yaml before
`rockcraft pack`, so the file is baked into the image (it lives under
templates/, which the rock primes).

Run locally with: python3 scripts/generate_llms.py
"""

import os
import sys

# Ensure the repo root is importable when run as `python3 scripts/...`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from webapp import llms  # noqa: E402
from webapp.app import LLMS_TXT, app  # noqa: E402


def main():
    content = llms.build_llms_full_txt(app, LLMS_TXT)
    file_path = os.path.join(os.getcwd(), "templates", "llms-full.txt")
    with open(file_path, "w") as f:
        f.write(content)
    print(f"generated {file_path} ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
