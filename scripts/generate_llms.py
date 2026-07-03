#!/usr/bin/env python3
"""Pre-generate llms.txt and llms-full.txt at build time.

Invoked from .github/workflows/deploy.yaml before `rockcraft pack`, so both
files are baked into the image (they live under templates/, which the rock
primes). Every pod then serves them instantly from disk instead of rendering
every page in a request context on prod — which times out for llms-full.txt.

Run locally with: python3 scripts/generate_llms.py
"""

import os
import sys

# Ensure the repo root is importable when run as `python3 scripts/...`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from webapp import llms  # noqa: E402
from webapp.app import app  # noqa: E402


def main():
    for key in llms.LLMS_FILES:
        content = llms.write_llms_file(app, key)
        print(
            f"generated {llms.LLMS_FILES[key]['filename']} "
            f"({len(content)} bytes)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
