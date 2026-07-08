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
  - PAGE_NAVIGATION : must mirror the heading structure in content.md.
                      It drives both the in-page navigation sidebar AND
                      the automatic h3 id injection (see _inject_heading_ids).
  - _DEF_TERMS      : must list every bold "Term:" in the Definitions section.
                      These are used to inject HTML id attributes on definition
                      terms so that #def-* anchor links resolve correctly.
"""
import os
import re

import markdown

# Update this string whenever the document is officially re-issued.
EFFECTIVE_DATE = "26 JUNE 2026"

# Drives the in-page navigation sidebar rendered by vf_in_page_navigation in
# index.html. The ids here must match the h2/h3 heading text in content.md
# (after stripping leading "N. " numbers) so that _inject_heading_ids can
# resolve them. If you rename a section or add/remove sub-sections, update
# both this structure and the corresponding headings in content.md.
PAGE_NAVIGATION = [
    {"id": "introduction", "text": "Introduction"},
    {
        "id": "security-compliance",
        "text": "Security and compliance",
        "children": [
            {"id": "expanded-security-maintenance", "text": "1. Expanded Security Maintenance (ESM)"},
            {"id": "legacy-add-on", "text": "2. Legacy add-on"},
            {"id": "other-security-fixes", "text": "3. Other security fixes"},
            {"id": "certified-components", "text": "4. Certified components for compliance, hardening and audit"},
            {"id": "kernel-livepatch", "text": "5. Kernel Livepatch"},
            {"id": "access-to-other-services", "text": "6. Access to other services"},
            {"id": "subscription-limitations", "text": "7. Subscription limitations"},
        ],
    },
    {
        "id": "support",
        "text": "Support",
        "children": [
            {"id": "scope-of-support", "text": "8. Scope of Support"},
            {"id": "supported-products", "text": "9. Supported Products"},
            {"id": "exclusions", "text": "10. Exclusions"},
        ],
    },
    {
        "id": "support-services-process",
        "text": "Support Services Process",
        "children": [
            {"id": "service-initiation", "text": "11. Service initiation"},
            {"id": "submitting-support-requests", "text": "12. Submitting support requests"},
            {"id": "support-severity-levels", "text": "13. Support severity levels"},
            {"id": "customer-assistance", "text": "14. Customer assistance"},
            {"id": "hotfixes", "text": "15. Hotfixes"},
            {"id": "support-language", "text": "16. Support language"},
            {"id": "remote-sessions", "text": "17. Remote sessions"},
            {"id": "ask-for-peer-review", "text": "18. Ask for a Peer Review"},
            {"id": "management-escalation", "text": "19. Management escalation"},
            {"id": "levels-of-support", "text": "20. Levels of Support"},
        ],
    },
    {
        "id": "add-ons",
        "text": "Add-Ons",
        "children": [
            {"id": "managed-services", "text": "21. Managed Services"},
            {"id": "firefighting-support", "text": "22. Firefighting Support"},
            {"id": "ops-consultancy", "text": "23. OpsConsultancy"},
            {"id": "professional-support-services", "text": "24. Professional Support Services"},
            {"id": "embedded-services", "text": "25. Embedded Services"},
        ],
    },
    {"id": "definitions", "text": "Definitions"},
]

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
    ("Expanded Security Maintenance (ESM)", "def-expanded-security-maintenance"),
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

_DELIMITER = re.compile(
    r"^<!-- section:\s*(\S+?)\s*-->[ \t]*$", re.MULTILINE
)


def _build_h3_id_map():
    """
    Build a lookup of {heading_text: nav_id} from PAGE_NAVIGATION children.

    The heading text key is the nav item text with the leading "N. " number
    stripped, e.g. "1. Expanded Security Maintenance (ESM)" becomes
    "Expanded Security Maintenance (ESM)".

    This is used by _inject_heading_ids to match rendered <h3> elements against
    nav ids without requiring {#id} attributes in content.md (which would need
    to be re-added every time the document is pasted from the Google Doc).
    """
    id_map = {}
    for item in PAGE_NAVIGATION:
        for child in item.get("children", []):
            text = re.sub(r"^\d+\.\s+", "", child["text"]).strip()
            id_map[text] = child["id"]
    return id_map


_H3_ID_MAP = _build_h3_id_map()


def _inject_heading_ids(html, sec_id):
    """
    Inject id attributes on headings so the in-page navigation sidebar can
    track the active section as the user scrolls.

    WHY: The vf_in_page_navigation macro's IntersectionObserver watches h2/h3
    elements and reads their .id property to determine which nav link to
    highlight. Without ids on the headings the observer always gets an empty
    string and no primary nav item ever activates.

    WHY NOT in content.md: Adding {#id} to headings in content.md works but
    requires re-adding them every time the document is updated from the Google
    Doc. Injecting them here keeps content.md paste-friendly.

    - The first <h2> in the section gets id=sec_id, which comes directly from
      the <!-- section: id --> delimiter in content.md.
    - <h3> headings are matched against PAGE_NAVIGATION via their visible text
      content (HTML tags stripped, leading "N. " number removed). If a match
      is found in _H3_ID_MAP, the corresponding nav id is injected.
    """
    html = html.replace("<h2>", f'<h2 id="{sec_id}">', 1)

    def inject_h3_id(m):
        inner = m.group(1)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        text = re.sub(r"^\d+\.\s+", "", text).strip()
        nav_id = _H3_ID_MAP.get(text)
        if nav_id:
            return f'<h3 id="{nav_id}">{inner}</h3>'
        return m.group(0)

    return re.sub(r"<h3>(.*?)</h3>", inject_h3_id, html, flags=re.DOTALL)


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
        html = _inject_heading_ids(html, sec_id)
        html = html.replace("<table>", '<table class="p-table">')
        if sec_id == "definitions":
            for term, def_id in _DEF_TERMS:
                html = html.replace(
                    f"<strong>{term}:</strong>",
                    f'<strong id="{def_id}">{term}:</strong>',
                )
        sections[sec_id] = html

    return sections
