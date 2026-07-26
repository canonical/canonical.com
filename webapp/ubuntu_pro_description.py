"""
Ubuntu Pro Description page helpers
====================================
This module owns all content-related data and rendering logic for
/legal/ubuntu-pro-description. The two Flask routes in app.py are thin
wrappers that call load_sections() and pass the results to the templates.

See the comment block at the top of content.md for editing conventions
(section delimiters, anchor link format, heading rules).

The key items to keep in sync when the document changes:

  - effective_date  : YAML frontmatter field in content.md; update it there
                      when the document is re-issued.
  - Definition terms: each bold "**Term:**" or "**Term**:" entry in the
                      Definitions section of content.md is automatically
                      detected and assigned a slug of the form def-<slug>,
                      where <slug> is derived by lowercasing the term text
                      and replacing non-alphanumeric characters with hyphens.
                      No Python-side list needs to be maintained.
"""

import os
import re

import markdown
import yaml
from slugify import slugify

_CONTENT_MD = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "templates",
    "legal",
    "ubuntu-pro-description",
    "content.md",
)

_DELIMITER = re.compile(r"^<!-- section:\s*(\S+?)\s*-->[ \t]*$", re.MULTILINE)

# Matches both
# **Term:** (colon inside bold) and
# **Term**: (colon outside bold)
# at the start of a line, as used for definition entries.
_DEF_TERM_RE = re.compile(r"^\*\*(.*?)(?::\*\*|\*\*:)", re.MULTILINE)

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _slugify_term(text):
    """Convert a definition term to a def-* HTML id slug."""
    return "def-" + slugify(text)


def load_sections(strip_h3_numbers=False):
    """
    Read content.md, parse optional YAML frontmatter, split on
    <!-- section: id --> markers, render each chunk to HTML, and
    return a ({section_id: html}, metadata) tuple where metadata is
    the parsed frontmatter dict (empty dict if none is present).

    Pass strip_h3_numbers=True for the print/PDF export view so that
    hardcoded clause numbers are removed from h3 headings and the CSS
    section-num counter can renumber them based on which sections are
    actually rendered.
    This is not done on the index page to allow the full-page scope
    in-page navigation to display h3 heading numbering
    """
    with open(_CONTENT_MD, encoding="utf-8") as f:
        raw = f.read()

    metadata = {}
    fm_match = _FRONTMATTER.match(raw)
    if fm_match:
        metadata = yaml.safe_load(fm_match.group(1)) or {}
        raw = raw.removeprefix(fm_match.group(0))

    parts = _DELIMITER.split(raw)
    # parts: [preamble, section_id, content, section_id, content, ...]

    sections = {}
    for i in range(1, len(parts), 2):
        sec_id = parts[i]
        sec_md = parts[i + 1] if i + 1 < len(parts) else ""
        html = markdown.markdown(
            sec_md.strip(),
            extensions=["tables", "attr_list", "sane_lists"],
            tab_length=3,
        )
        html = html.replace("<table>", '<table class="p-table">')
        if strip_h3_numbers:
            # Strip hardcoded clause numbers (e.g. "8. ") from h3 headings.
            # The CSS section-num counter re-applies them dynamically so that
            # the numbering stays correct when only a subset of sections is
            # rendered in the print/PDF export view.
            html = re.sub(r"(<h3>)\d+\.\s*", r"\1", html)
        # Python Markdown wraps <li> content in <p> for "loose"
        # lists (lists with blank lines between items). This causes
        # the counter ::before to appear on a separate line from the text.
        # Strip the <p> wrapper from items that have exactly one paragraph,
        # optionally followed by a sub-list. Multi-paragraph items are left
        # unchanged.
        html = re.sub(
            r"<li>\s*<p>((?:(?!</li>).)*?)</p>(\s*<(?:ol|ul|table|/li))",
            r"<li>\1\2",
            html,
            flags=re.DOTALL,
        )
        if sec_id == "support-services-process":
            html = html.replace(
                '<table class="p-table">',
                '<div class="p-sev-table-wrap"><table class="p-table">',
            )
            html = html.replace("</table>", "</table></div>")
        if sec_id == "definitions":
            for match in _DEF_TERM_RE.finditer(sec_md):
                term = match.group(1)
                def_id = _slugify_term(term)
                # Handle colon inside bold: **Term:** → <strong>Term:</strong>
                html = html.replace(
                    f"<strong>{term}:</strong>",
                    f'<strong id="{def_id}">{term}:</strong>',
                )
                # Handle colon outside bold: **Term**: → <strong>Term</strong>:
                html = html.replace(
                    f"<strong>{term}</strong>:",
                    f'<strong id="{def_id}">{term}</strong>:',
                )
        sections[sec_id] = html

    return sections, metadata
