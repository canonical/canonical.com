#!/usr/bin/env python3
"""
One-shot migration: replace every `style="..."` attribute across the
templates with a `class="s-<hash6>"` reference, and emit one SCSS
partial that defines each unique class. Run once.

Why this shape:
- CSP `style-src 'unsafe-inline'` covers BOTH `<style>` blocks and
  `style=""` attrs. Nonces work for blocks but not attrs (there's no
  way to nonce an attribute), so to drop 'unsafe-inline' entirely we
  have to migrate every attr to a stylesheet rule.
- Most of the inline styles are duplicates (60 × `text-wrap: wrap`,
  28 × `scroll-margin-top: 3.5rem`, etc.). A content-hash class name
  collapses the 357 instances into ~95 stable classes with zero risk
  of accidental collision between templates.

Edge cases handled:
- Existing `class="..."` on the same element → the new `s-<hash6>` is
  appended; we never overwrite an existing class list.
- Jinja blocks (`{{ ... }}`, `{% ... %}`) are stashed out before
  parsing so brace characters inside expressions can't break the
  attribute matcher.

Outputs:
- `static/sass/_inline-styles-migration.scss` — one rule per class.
- Modified template files (only those containing `style=""`).
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATES = REPO / "templates"
SCSS_OUT = REPO / "static" / "sass" / "_inline-styles-migration.scss"

# Jinja stashing: prevents `{{ ... }}` / `{% ... %}` from confusing the
# attribute matcher when a template expression appears inside an HTML
# attribute list.
JINJA_BLOCK = re.compile(r"\{\{.*?\}\}|\{%.*?%\}", re.DOTALL)

# Matches `class="..."` and `style="..."` attributes. Quoting is "
# everywhere in our templates (verified by audit).
CLASS_ATTR = re.compile(r'\bclass="([^"]*)"')
STYLE_ATTR = re.compile(r'\bstyle="([^"]*)"')


def normalise(css: str) -> str:
    """Canonical form of a CSS declaration list — strip surrounding
    whitespace, collapse internal whitespace runs, drop trailing
    semicolons, and standardise spacing around `;`.
    """
    s = re.sub(r"\s+", " ", css).strip().rstrip(";").strip()
    s = re.sub(r"\s*;\s*", "; ", s)
    return s


def class_for(css: str) -> str:
    """Stable 6-char hash class name for a CSS declaration list."""
    h = hashlib.sha1(css.encode("utf-8")).hexdigest()[:6]
    return f"s-{h}"


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


def migrate_file(
    path: Path, css_to_class: dict[str, str]
) -> tuple[int, set[str]]:
    """Mutate one template in-place. Returns (rewrite_count, classes_used)."""
    src = path.read_text()
    stashed, jinja_parts = stash_jinja(src)
    used: set[str] = set()
    count = 0

    # Helper: append `cls` to the existing class attribute on the tag
    # that contains `style_pos`, or insert a fresh class attribute next
    # to the style attribute if there isn't one.
    def merge_class_into_tag(tag: str, cls: str) -> str:
        m = CLASS_ATTR.search(tag)
        if m:
            existing = m.group(1).strip()
            if cls in existing.split():
                return tag  # already there
            new_attr = f'class="{(existing + " " + cls).strip()}"'
            return tag[: m.start()] + new_attr + tag[m.end() :]
        # No class attribute — add one right where style was.
        # We rely on the caller having already removed `style="..."` so
        # we insert at the location of the removed style attribute.
        return tag

    # Build the new source by walking through tags. The matcher finds
    # `<tag ... style="..." ...>`, and we transform the whole tag.
    TAG = re.compile(r"<[^>]*?style=\"[^\"]*\"[^>]*>", re.DOTALL)

    def transform_tag(m: re.Match) -> str:
        nonlocal count
        tag = m.group(0)
        # There may be more than one style attr on the same opening tag
        # (rare, but cheap to handle).
        while True:
            sm = STYLE_ATTR.search(tag)
            if not sm:
                break
            css = normalise(sm.group(1))
            if not css:
                # Empty style="" — just drop the attribute.
                tag = (tag[: sm.start()] + tag[sm.end() :]).replace(
                    "  ", " "
                )
                continue
            cls = css_to_class.setdefault(css, class_for(css))
            used.add(cls)
            # Remove the style attribute, then merge class.
            tag_no_style = (
                tag[: sm.start()] + tag[sm.end() :]
            ).replace("  ", " ")
            tag = merge_class_into_tag(tag_no_style, cls)
            # If there was no class attribute, insert one right before
            # the closing `>` to avoid breaking attribute ordering.
            if cls not in tag:
                tag = tag.rstrip("/>") + f' class="{cls}"' + (
                    "/>" if m.group(0).endswith("/>") else ">"
                )
            count += 1
        # Collapse any double spaces left from attribute removal.
        return re.sub(r" {2,}", " ", tag)

    new_stashed = TAG.sub(transform_tag, stashed)
    new_src = restore_jinja(new_stashed, jinja_parts)

    if new_src != src:
        path.write_text(new_src)
    return count, used


def emit_scss(css_to_class: dict[str, str]) -> None:
    """Write the SCSS partial with one rule per unique class."""
    # Sort so the file is stable across re-runs.
    items = sorted(css_to_class.items())
    lines = [
        "// Generated by scripts/migrate_inline_styles.py — do not hand-edit.",
        "// Each class corresponds to one unique inline `style=\"...\"` that",
        "// previously appeared in templates. Generated to let us drop",
        "// 'unsafe-inline' from CSP style-src.",
        "",
    ]
    for css, cls in items:
        # CSS body is already a valid declaration list; just wrap it.
        lines.append(f".{cls} {{ {css}; }}")
    lines.append("")
    SCSS_OUT.write_text("\n".join(lines))


def main() -> int:
    css_to_class: dict[str, str] = {}
    total = 0
    files_touched = 0
    classes_used: set[str] = set()

    files = sorted(TEMPLATES.rglob("*.html")) + sorted(
        TEMPLATES.rglob("*.md")
    )
    for f in files:
        n, used = migrate_file(f, css_to_class)
        if n:
            files_touched += 1
            total += n
            classes_used |= used

    emit_scss({c: cls for c, cls in css_to_class.items() if cls in classes_used})

    print(f"Total inline-style rewrites: {total}")
    print(f"Files modified:              {files_touched}")
    print(f"Unique classes emitted:      {len(classes_used)}")
    print(f"SCSS partial written:        {SCSS_OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
