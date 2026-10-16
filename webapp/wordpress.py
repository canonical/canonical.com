"""Consume WordPress Gutenberg content and map it to the Vanilla ``vf_hero``
macro schema.

This is a bare-bones demo of the "edit in WordPress -> REST API -> vf_hero
render" pipeline. A hero is authored in wp-admin as a *pattern* built from core
Gutenberg blocks (no custom block plugin, no ACF yet). Flask fetches the raw
block markup for a page (``GET /wp-json/wp/v2/pages/<id>?context=edit``, which
requires authentication with a WordPress application password), parses the
serialized block markup here, and maps it into the exact ``blocks=[]``
shape the ``vf_hero`` Jinja macro expects.

The pattern must follow a fixed structure for the mapping to be deterministic:

* A top-level ``core/group`` whose Additional CSS class encodes the
  layout, e.g. ``hero-layout--50-50`` (see ``_LAYOUT_CLASS_PREFIX``).
  Missing/unknown -> ``fallback``.
* Inside the group, in order:
    * ``core/heading`` level 1  -> ``title_text`` (required)
    * ``core/heading`` level 2  -> ``subtitle_text`` (optional)
    * ``core/paragraph`` (any)  -> one ``description`` block each
    * ``core/buttons``          -> one ``cta-block`` (first button = primary,
                                   next up to two = secondaries)
    * ``core/image``            -> ``image`` block (a second image with
                                   the ``signpost`` class becomes the
                                   ``signpost_image`` block)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any, Optional


class WordPressError(Exception):
    """Raised when the WordPress REST API response cannot be used."""


# --- Block markup parsing --------------------------------------------------

# Matches a Gutenberg block delimiter comment, e.g.
#   <!-- wp:heading {"level":1} -->
#   <!-- /wp:heading -->
#   <!-- wp:spacer {"height":"20px"} /-->
# The attributes group is captured loosely and validated with json.loads later.
# Matches the opening of a Gutenberg block delimiter comment, e.g.
#   <!-- wp:heading ...
#   <!-- /wp:heading ...
# The attributes JSON and closing "-->" (and any "/-->" void marker) are parsed
# manually after this match so that nested JSON objects (e.g. a group block's
# "layout" object) are handled correctly - a non-greedy regex would truncate at
# the first "}".
_DELIM_START_RE = re.compile(
    r"<!--\s+"
    r"(?P<closer>/)?"
    r"wp:(?P<name>[a-z][a-z0-9_-]*(?:/[a-z][a-z0-9_-]*)?)"
)

_WHITESPACE = " \t\r\n"


@dataclass
class Block:
    """A parsed Gutenberg block."""

    name: str
    attrs: dict[str, Any] = field(default_factory=dict)
    inner_html: str = ""
    inner_blocks: list["Block"] = field(default_factory=list)


def _normalize_name(name: str) -> str:
    """Core blocks serialize without the ``core/`` namespace; add it back so
    callers can match on a single canonical name."""
    return name if "/" in name else f"core/{name}"


def _scan_json_object(content: str, start: int) -> tuple[Optional[str], int]:
    """Return the balanced ``{...}`` substring starting at ``content[start]``
    (which must be ``{``) and the index just past it. String contents (and
    escaped quotes) are respected so braces inside strings do not count.

    Returns ``(None, start)`` if no balanced object is found.
    """
    depth = 0
    in_string = False
    escaped = False
    i = start
    while i < len(content):
        char = content[i]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return content[start : i + 1], i + 1
        i += 1
    return None, start


def parse_blocks(content: str) -> list[Block]:
    """Parse serialized Gutenberg block markup into a tree of :class:`Block`.

    Freeform content outside of block delimiters is ignored (it is not
    relevant to the structured hero mapping).
    """
    root_children: list[Block] = []
    # Stack of (block, html_fragments) frames; the last frame is the current
    # open block whose inner HTML we are accumulating.
    stack: list[tuple[Optional[Block], list[str]]] = [(None, [])]
    pos = 0

    while True:
        match = _DELIM_START_RE.search(content, pos)
        if match is None:
            break

        # Text since the previous delimiter belongs to the current open block.
        stack[-1][1].append(content[pos : match.start()])

        is_closer = match.group("closer") is not None
        name = _normalize_name(match.group("name"))

        cursor = match.end()
        while cursor < len(content) and content[cursor] in _WHITESPACE:
            cursor += 1

        attrs: dict[str, Any] = {}
        if cursor < len(content) and content[cursor] == "{":
            raw_attrs, cursor = _scan_json_object(content, cursor)
            if raw_attrs:
                try:
                    attrs = json.loads(raw_attrs)
                except json.JSONDecodeError:
                    attrs = {}

        while cursor < len(content) and content[cursor] in _WHITESPACE:
            cursor += 1

        is_void = content.startswith("/", cursor)
        if is_void:
            cursor += 1

        end = content.find("-->", cursor)
        if end == -1:
            break
        pos = end + 3

        if is_closer:
            block, fragments = stack.pop()
            if block is not None:
                block.inner_html = "".join(fragments).strip()
                parent_children = (
                    stack[-1][0].inner_blocks
                    if stack[-1][0]
                    else root_children
                )
                parent_children.append(block)
            continue

        block = Block(name=name, attrs=attrs)

        if is_void:
            parent_children = (
                stack[-1][0].inner_blocks if stack[-1][0] else root_children
            )
            parent_children.append(block)
        else:
            stack.append((block, []))

    return root_children


def iter_blocks(blocks: list[Block]):
    """Depth-first iterator over a block tree."""
    for block in blocks:
        yield block
        yield from iter_blocks(block.inner_blocks)


# --- Small HTML helpers ----------------------------------------------------


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self._parts.append(data)

    @property
    def text(self) -> str:
        return "".join(self._parts).strip()


def _text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    return parser.text


class _FirstTagFinder(HTMLParser):
    """Collect attributes of the first occurrence of a given tag."""

    def __init__(self, tag: str) -> None:
        super().__init__()
        self._tag = tag
        self.attrs: Optional[dict[str, str]] = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if self.attrs is None and tag == self._tag:
            self.attrs = {k: (v or "") for k, v in attrs}


def _first_tag_attrs(html: str, tag: str) -> dict[str, str]:
    finder = _FirstTagFinder(tag)
    finder.feed(html)
    return finder.attrs or {}


_ASPECT_RE = re.compile(r"\baspect--(16-9|3-2|2-3|cinematic)\b")

_LAYOUT_CLASS_PREFIX = "hero-layout--"
_VALID_LAYOUTS = {
    "50-50",
    "50-50-full-width-image",
    "75-25",
    "25-75",
    "fallback",
}


def _layout_from_group(group: Block) -> str:
    # vf_hero normalizes "/" to "-" and validates against the dash forms,
    # so the dash form read straight off the CSS class passes through.
    class_name = str(group.attrs.get("className", ""))
    for token in class_name.split():
        if token.startswith(_LAYOUT_CLASS_PREFIX):
            layout = token[len(_LAYOUT_CLASS_PREFIX) :]
            if layout in _VALID_LAYOUTS:
                return layout
    return "fallback"


def _description_block(paragraph: Block) -> dict[str, Any]:
    return {
        "type": "description",
        "item": {"type": "html", "content": paragraph.inner_html},
    }


def _cta_item_from_button(button: Block) -> dict[str, Any]:
    attrs = _first_tag_attrs(button.inner_html, "a")
    item: dict[str, Any] = {"content_html": _text(button.inner_html)}
    href = attrs.get("href")
    if href:
        item["attrs"] = {"href": href}
    return item


def _cta_block(buttons: Block) -> Optional[dict[str, Any]]:
    button_blocks = [
        b for b in buttons.inner_blocks if b.name == "core/button"
    ]
    if not button_blocks:
        return None
    item: dict[str, Any] = {"primary": _cta_item_from_button(button_blocks[0])}
    secondaries = [_cta_item_from_button(b) for b in button_blocks[1:3]]
    if secondaries:
        item["secondaries"] = secondaries
    return {"type": "cta-block", "item": item}


def _image_block(image: Block, block_type: str = "image") -> dict[str, Any]:
    img = _first_tag_attrs(image.inner_html, "img")
    attrs: dict[str, str] = {}
    if img.get("src"):
        attrs["src"] = img["src"]
    attrs["alt"] = img.get("alt", "")
    if img.get("width"):
        attrs["width"] = img["width"]
    if img.get("height"):
        attrs["height"] = img["height"]

    item: dict[str, Any] = {"attrs": attrs}
    class_name = str(image.attrs.get("className", ""))
    aspect = _ASPECT_RE.search(class_name)
    if aspect:
        item["aspect_ratio"] = aspect.group(1)
    return {"type": block_type, "item": item}


def _is_signpost(image: Block) -> bool:
    return "signpost" in str(image.attrs.get("className", "")).split()


def _has_layout_class(group: Block) -> bool:
    class_name = str(group.attrs.get("className", ""))
    for token in class_name.split():
        if token.startswith(_LAYOUT_CLASS_PREFIX):
            if token[len(_LAYOUT_CLASS_PREFIX) :] in _VALID_LAYOUTS:
                return True
    return False


def _find_hero_group(blocks: list[Block]) -> Optional[Block]:
    """Locate the group that holds the hero content.

    The WordPress editor commonly wraps pasted/patterned content in an extra
    outer ``core/group``, so we cannot just take the first group. Prefer a
    group carrying a valid ``hero-layout--*`` class; otherwise fall back to a
    group that directly contains an H1 heading; otherwise the first group.
    """
    groups = [b for b in iter_blocks(blocks) if b.name == "core/group"]
    if not groups:
        return None

    for group in groups:
        if _has_layout_class(group):
            return group

    for group in groups:
        if any(
            child.name == "core/heading" and child.attrs.get("level") == 1
            for child in group.inner_blocks
        ):
            return group

    return groups[0]


def map_hero(blocks: list[Block]) -> Optional[dict[str, Any]]:
    """Map a parsed block tree to the ``vf_hero`` keyword-argument shape.

    Returns ``None`` if no hero group / title can be found.
    """
    group = _find_hero_group(blocks)
    if group is None:
        return None

    title_text = ""
    subtitle_text = ""
    hero_blocks: list[dict[str, Any]] = []
    images: list[Block] = []

    for block in group.inner_blocks:
        if block.name == "core/heading":
            level = block.attrs.get("level", 2)
            if level == 1 and not title_text:
                title_text = _text(block.inner_html)
            elif level == 2 and not subtitle_text:
                subtitle_text = _text(block.inner_html)
        elif block.name == "core/paragraph":
            if block.inner_html:
                hero_blocks.append(_description_block(block))
        elif block.name == "core/buttons":
            cta = _cta_block(block)
            if cta:
                hero_blocks.append(cta)
        elif block.name == "core/image":
            images.append(block)

    if not title_text:
        return None

    for image in images:
        if _is_signpost(image):
            hero_blocks.append(_image_block(image, "signpost_image"))
        else:
            hero_blocks.append(_image_block(image, "image"))

    hero: dict[str, Any] = {
        "title_text": title_text,
        "layout": _layout_from_group(group),
        "blocks": hero_blocks,
    }
    if subtitle_text:
        hero["subtitle_text"] = subtitle_text
    return hero


# --- Fetching --------------------------------------------------------------


def fetch_page_raw_content(session, api_url, user, app_password, page_id):
    """Fetch a page's raw Gutenberg block markup from the WordPress REST API.

    ``context=edit`` (required to receive ``content.raw``) needs
    authentication; WordPress application passwords use HTTP Basic auth.
    """
    url = f"{api_url.rstrip('/')}/wp-json/wp/v2/pages/{page_id}"
    response = session.get(
        url,
        params={"context": "edit"},
        auth=(user, app_password),
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    content = data.get("content", {})
    if "raw" not in content:
        # ``content.raw`` is only returned for authenticated ?context=edit
        # requests. Its absence means the request was treated as
        # unauthenticated (wrong/blank app password, or no edit access).
        raise WordPressError(
            "WordPress returned no 'content.raw' for page "
            f"{page_id}. Check WORDPRESS_USERNAME / "
            "WORDPRESS_APPLICATION_PASSWORD and that the user can edit "
            "the page."
        )
    return content["raw"]


def get_hero_from_page(session, api_url, user, app_password, page_id):
    """Fetch, parse, and map a WordPress page into the ``vf_hero`` shape."""
    raw = fetch_page_raw_content(session, api_url, user, app_password, page_id)
    return map_hero(parse_blocks(raw))
