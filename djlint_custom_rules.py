"""Custom djlint linter rules for canonical.com.

Loaded by djlint via ``.djlint_rules.yaml`` (``python_module`` rules). Unlike
djlint pattern rules, ``python_module`` rules receive the full HTML and are not
filtered by djlint's ignored-block logic, so they can inspect ``<script>`` tags
(which djlint otherwise treats as ignored blocks).
"""

from __future__ import annotations

import re

from djlint.lint import get_line

# Match a single <script ...> opening tag.
SCRIPT_OPEN_TAG = re.compile(r"<script\b[^>]*>", re.IGNORECASE)
HAS_SRC = re.compile(r"\bsrc=", re.IGNORECASE)
HAS_NONCE = re.compile(r"\bnonce\b", re.IGNORECASE)


def run(rule, config, html, filepath, line_ends, *args, **kwargs):
    """C001: <script src=...> tags must include a nonce= attribute."""
    errors = []
    for match in SCRIPT_OPEN_TAG.finditer(html):
        tag = match.group()
        if not HAS_SRC.search(tag):
            continue
        if HAS_NONCE.search(tag):
            continue
        snippet = re.sub(r"\s+", " ", tag)[:30]
        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": snippet,
            "message": rule["message"],
        })
    return errors
