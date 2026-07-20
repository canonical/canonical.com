"""
Ubuntu Pro Description page helpers
====================================
This module owns all content-related data and rendering logic for
/legal/ubuntu-pro-description. The two Flask routes in app.py are thin
wrappers that call load_sections() and pass the results to the templates.

See the comment block at the top of content.md for editing conventions
(section delimiters, anchor link format, heading rules).

The key items to keep in sync when the document changes:

  - EFFECTIVE_DATE  : update when the document is re-issued.
  - _DEF_TERMS      : must list every bold "Term:" in the Definitions section.
                      These are used to inject HTML id attributes on definition
                      terms so that #def-* anchor links resolve correctly.
"""

import os
import re

import markdown

# Update this string whenever the document is officially re-issued.
EFFECTIVE_DATE = "26 JUNE 2026"

# Python Markdown renders "**Term:**" as "<strong>Term:</strong>" with no id
# attribute. We need ids so that #def-* anchor links in the body text can
# resolve to the correct definition entry. This list drives a post-render
# string replacement that injects id="def-*" on each matching <strong> tag.
#
# Keep this list in sync with the Definitions section of content.md.
# Add an entry here whenever a new definition is added to the document.
_DEF_TERMS = [
    ("Applications", "def-applications"),
    ("Break-fix Support", "def-break-fix-support"),
    ("Bug-fix Support", "def-bug-fix-support"),
    ("Business Hours", "def-business-hours"),
    ("Ceph Cluster", "def-ceph-cluster"),
    ("Certified Hardware", "def-certified-hardware"),
    ("Charm", "def-charm"),
    ("Charmed Kubernetes", "def-charmed-kubernetes"),
    ("Covered Architectures", "def-covered-architectures"),
    ("CVEs (High and Critical)", "def-cves-high-and-critical"),
    ("Desktop use case", "def-desktop-use-case"),
    ("Device use case", "def-device-use-case"),
    ("Enabled kernel", "def-enabled-kernel"),
    ("Environment", "def-environment"),
    ("End of Life", "def-end-of-life"),
    ("End of Standard Support", "def-end-of-standard-support"),
    ("Expanded Security Maintenance (ESM)", "def-esm"),
    ("Infra support", "def-infra-support"),
    ("Knowledge Base", "def-knowledge-base"),
    ("Kubernetes", "def-kubernetes"),
    ("Node", "def-node"),
    ("OpenStack", "def-openstack"),
    ("Release date", "def-release-date"),
    ("Troubleshooting", "def-troubleshooting"),
    ("Ubuntu Archive", "def-ubuntu-archive"),
    ("Ubuntu Core", "def-ubuntu-core"),
    ("Ubuntu Guest", "def-ubuntu-guest"),
    ("Ubuntu Main", "def-ubuntu-main"),
    ("Ubuntu Universe", "def-ubuntu-universe"),
    ("Valid Customisations", "def-valid-customisations"),
]

_CONTENT_MD = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "templates",
    "legal",
    "ubuntu-pro-description",
    "content.md",
)

_DELIMITER = re.compile(r"^<!-- section:\s*(\S+?)\s*-->[ \t]*$", re.MULTILINE)


def load_sections():
    """
    Read content.md, split on <!-- section: id --> markers, render each chunk
    to HTML, and return a {section_id: html} dict.
    """
    with open(_CONTENT_MD, encoding="utf-8") as f:
        raw = f.read()

    parts = _DELIMITER.split(raw)
    # parts: [preamble, section_id, content, section_id, content, ...]

    sections = {}
    for i in range(1, len(parts), 2):
        sec_id = parts[i]
        sec_md = parts[i + 1] if i + 1 < len(parts) else ""
        html = markdown.markdown(
            sec_md.strip(),
            extensions=["tables", "attr_list", "sane_lists"],
        )
        html = html.replace("<table>", '<table class="p-table">')
        if sec_id == "support-services-process":
            html = html.replace(
                '<table class="p-table">',
                '<div class="p-sev-table-wrap"><table class="p-table">',
            )
            html = html.replace("</table>", "</table></div>")
        if sec_id == "definitions":
            for term, def_id in _DEF_TERMS:
                html = html.replace(
                    f"<strong>{term}:</strong>",
                    f'<strong id="{def_id}">{term}:</strong>',
                )
        sections[sec_id] = html

    return sections
