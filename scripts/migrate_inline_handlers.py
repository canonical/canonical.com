#!/usr/bin/env python3
"""
One-shot migration: rewrite inline on*= attributes in the templates we
inventoried into the declarative data-* conventions consumed by
static/js/csp-handlers.js.

This script is checked in so the diff it produces is reproducible; it
isn't wired into CI and should be run at most once.

Handled cases (in order of recognition per attribute):

  1. onclick="dataLayer.push({...});"                  → data-ga-*
  2. onclick="dataLayer.push({A}); dataLayer.push({B});" → data-ga-* + data-ga-extra-*
  3. onclick="document.querySelector('#x').classList.add('u-hide');" → data-dismiss="#x"
  4. onclick="this.previousElementSibling.value = '';
            this.previousElementSibling.focus();"      → data-action="clear-prev-input"
  5. onclick="showProgressDetail('foo'); event.preventDefault();"
                                                       → data-progress-action="show" data-progress-target="foo"
  6. onclick="hideProgressDetail('foo'); event.preventDefault();"
                                                       → data-progress-action="hide" data-progress-target="foo"
  7. onclick="loadMoreResults()"                       → data-action="load-more-results"
  8. onchange="showInput()"                            → data-on-change="showInput"
  9. onsubmit="getCustomFields(event)"                 → data-on-submit="getCustomFields"
 10. onsubmit="ga('send', 'X', 'Y', 'Z');"             → data-ga-submit-category / -action / -label

Anything not recognized is left in place and reported so we can review.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATES = REPO / "templates"

# --- Jinja stashing ----------------------------------------------------------
# Templates contain Jinja expressions like `{{ job.title }}` and `{% if %}`
# blocks. Their `{`/`}` characters confuse JS-style regex matching, so we
# replace each block with a sentinel before rewriting, then put it back.

JINJA_BLOCK = re.compile(r"\{\{.*?\}\}|\{%.*?%\}", re.DOTALL)


def stash_jinja(text: str) -> tuple[str, list[str]]:
    parts: list[str] = []

    def repl(m: re.Match) -> str:
        parts.append(m.group(0))
        return f"__JINJA{len(parts) - 1}__"

    return JINJA_BLOCK.sub(repl, text), parts


def restore_jinja(text: str, parts: list[str]) -> str:
    for i, part in enumerate(parts):
        text = text.replace(f"__JINJA{i}__", part)
    return text


# --- DataLayer parsing -------------------------------------------------------

# Captures one `dataLayer.push({...})` call. `re.DOTALL` so multi-line
# attributes (e.g. the job-application form's onsubmit) match.
DL_PUSH = re.compile(r"dataLayer\.push\(\{([^}]*)\}\s*\)\s*;?", re.DOTALL)

# Inside a dict body, capture `key : value` or `"key": "value"` pairs.
# Keys are unquoted in our templates (already-decoded) so the LHS can be
# bare word or quoted.
DL_PAIR = re.compile(
    r"""['"]?(event|eventCategory|eventAction|eventLabel)['"]?\s*:\s*['"]([^'"]+)['"]"""
)


def parse_datalayer_calls(js: str) -> list[dict]:
    """Return a list of dicts, one per dataLayer.push() found in `js`."""
    events = []
    for match in DL_PUSH.finditer(js):
        body = match.group(1)
        pairs = dict(DL_PAIR.findall(body))
        if "event" in pairs:
            events.append(pairs)
    return events


# --- Per-attribute rewriters -------------------------------------------------


def rewrite_onclick(raw: str) -> str | None:
    """Map an `onclick` value to a space-prefixed run of `data-*` attrs."""
    # Repair a pre-existing typo on /maas/features (`&quo;` → `&quot;`).
    # The handler at that site has been silently broken; fix it as part
    # of the migration so the analytics event starts firing again.
    raw = raw.replace("&quo;", "&quot;")
    # HTML-decode &quot;, etc. so the JS body is canonical.
    js = html.unescape(raw).strip().rstrip(";").strip()

    # (1) + (2) dataLayer.push — single or stacked
    if "dataLayer.push" in js:
        events = parse_datalayer_calls(js)
        if not events:
            return None
        out = (
            f' data-ga-event="{events[0].get("event", "")}"'
            f' data-ga-category="{events[0].get("eventCategory", "")}"'
            f' data-ga-action="{events[0].get("eventAction", "")}"'
            f' data-ga-label="{events[0].get("eventLabel", "")}"'
        )
        if len(events) > 1:
            out += (
                f' data-ga-extra-event="{events[1].get("event", "")}"'
                f' data-ga-extra-category="{events[1].get("eventCategory", "")}"'
                f' data-ga-extra-action="{events[1].get("eventAction", "")}"'
                f' data-ga-extra-label="{events[1].get("eventLabel", "")}"'
            )
        return out

    # (3) Notification dismissal
    m = re.match(
        r"document\.querySelector\(['\"](#[^'\"]+)['\"]\)\.classList\.add\(['\"]u-hide['\"]\)",
        js,
    )
    if m:
        return f' data-dismiss="{m.group(1)}"'

    # (4) Clear-previous-input
    if re.match(
        r"this\.previousElementSibling\.value\s*=\s*['\"]['\"]\s*;\s*"
        r"this\.previousElementSibling\.focus\(\)",
        js,
    ):
        return ' data-action="clear-prev-input"'

    # (5) Progress show
    m = re.match(
        r"showProgressDetail\(['\"]([^'\"]+)['\"]\)(?:\s*;\s*event\.preventDefault\(\))?",
        js,
    )
    if m:
        return (
            f' data-progress-action="show"'
            f' data-progress-target="{m.group(1)}"'
        )

    # (6) Progress hide
    m = re.match(
        r"hideProgressDetail\(['\"]([^'\"]+)['\"]\)(?:\s*;\s*event\.preventDefault\(\))?",
        js,
    )
    if m:
        return (
            f' data-progress-action="hide"'
            f' data-progress-target="{m.group(1)}"'
        )

    # (7) Load-more results
    if re.match(r"loadMoreResults\(\)", js):
        return ' data-action="load-more-results"'

    return None


def rewrite_onchange(raw: str) -> str | None:
    js = html.unescape(raw).strip().rstrip(";").strip()
    m = re.match(r"([A-Za-z_$][\w$]*)\(\)$", js)
    if m:
        return f' data-on-change="{m.group(1)}"'
    return None


def rewrite_onsubmit(raw: str) -> str | None:
    js = html.unescape(raw).strip().rstrip(";").strip()

    # dataLayer.push({event: "GAEvent", ...}) — single push only.
    if "dataLayer.push" in js:
        events = parse_datalayer_calls(js)
        if events:
            ev = events[0]
            return (
                f' data-ga-submit-event="{ev.get("event", "")}"'
                f' data-ga-submit-category="{ev.get("eventCategory", "")}"'
                f' data-ga-submit-action="{ev.get("eventAction", "")}"'
                f' data-ga-submit-label="{ev.get("eventLabel", "")}"'
            )

    # Legacy ga('send', 'X', 'Y', 'Z')
    m = re.match(
        r"ga\(\s*['\"]send['\"]\s*,\s*['\"]([^'\"]*)['\"]\s*,\s*"
        r"['\"]([^'\"]*)['\"]\s*,\s*['\"]([^'\"]*)['\"]\s*\)",
        js,
    )
    if m:
        return (
            f' data-ga-submit-category="{m.group(1)}"'
            f' data-ga-submit-action="{m.group(2)}"'
            f' data-ga-submit-label="{m.group(3)}"'
        )

    # name(event) — generic hook
    m = re.match(r"([A-Za-z_$][\w$]*)\(\s*event\s*\)$", js)
    if m:
        return f' data-on-submit="{m.group(1)}"'
    return None


REWRITERS = {
    "onclick": rewrite_onclick,
    "onchange": rewrite_onchange,
    "onsubmit": rewrite_onsubmit,
}

# Matches a single `onevent="..."` attribute (handles both " and ').
ATTR = re.compile(
    r"""\s+(on(?:click|change|submit))=(?P<q>["'])(?P<val>(?:(?!\2).)*)\2""",
    re.DOTALL,
)


def migrate_file(path: Path) -> tuple[int, list[str]]:
    src = path.read_text()
    rewrites = 0
    leftover: list[str] = []

    # Replace Jinja expressions with sentinels so the regex parser doesn't
    # trip on `{{ }}` inside attribute values (eventLabel templates).
    stashed_src, jinja_parts = stash_jinja(src)

    def repl(m: re.Match) -> str:
        nonlocal rewrites
        attr = m.group(1)
        val = m.group("val")
        replacement = REWRITERS[attr](val)
        if replacement is None:
            leftover.append(
                f"{path}: {attr}={restore_jinja(val, jinja_parts)[:120]!r}"
            )
            return m.group(0)  # leave untouched
        rewrites += 1
        return replacement

    new_stashed = ATTR.sub(repl, stashed_src)
    new_src = restore_jinja(new_stashed, jinja_parts)
    if new_src != src:
        path.write_text(new_src)
    return rewrites, leftover


def main() -> int:
    total_rewrites = 0
    all_leftover: list[str] = []
    files = sorted(TEMPLATES.rglob("*.html")) + sorted(
        TEMPLATES.rglob("*.md")
    )
    for f in files:
        n, left = migrate_file(f)
        if n:
            print(f"  {f.relative_to(REPO)}: {n} rewrites")
        total_rewrites += n
        all_leftover.extend(left)

    print(f"\nTotal rewrites: {total_rewrites}")
    if all_leftover:
        print(f"\nUnrecognized handlers ({len(all_leftover)}):")
        for line in all_leftover:
            print(f"  {line}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
