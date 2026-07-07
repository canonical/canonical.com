"""Enforce that every ``<script src=...>`` tag in templates carries a
``nonce=`` attribute (required by our Content-Security-Policy).

This lives in the standard test suite rather than as a djlint ``python_module``
rule because djlint strips ``<script>`` blocks before applying pattern rules,
which previously forced a custom module that was awkward to load in editors.
"""

import re
import unittest
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# Match a single <script ...> opening tag (may span multiple lines).
SCRIPT_OPEN_TAG = re.compile(r"<script\b[^>]*>", re.IGNORECASE | re.DOTALL)
HAS_SRC = re.compile(r"\bsrc=", re.IGNORECASE)
HAS_NONCE = re.compile(r"\bnonce\b", re.IGNORECASE)


class TestScriptNonce(unittest.TestCase):
    def test_script_src_tags_have_nonce(self):
        violations = []
        for path in TEMPLATES_DIR.rglob("*.html"):
            html = path.read_text(encoding="utf-8")
            for match in SCRIPT_OPEN_TAG.finditer(html):
                tag = match.group()
                if not HAS_SRC.search(tag):
                    continue
                if HAS_NONCE.search(tag):
                    continue
                line = html.count("\n", 0, match.start()) + 1
                rel = path.relative_to(TEMPLATES_DIR.parent)
                violations.append(f"{rel}:{line}")

        self.assertEqual(
            violations,
            [],
            "Script tags with src= must include a nonce= attribute:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
