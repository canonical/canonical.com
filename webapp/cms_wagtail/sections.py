"""Reshape Wagtail API blocks into the arguments the Vanilla macros expect.

A port of the StructValue helpers in sites-cms `website/blocks.py`. The
Vanilla macros are .jinja files, which Flask does not autoescape, so every
plain string bound for a macro is escaped here and only sanitised rich
text is marked safe. `value` stays raw: .html templates autoescape it.
"""

import re

import bleach
from canonicalwebteam import image_template
from markupsafe import Markup, escape

# What Wagtail's RICH_TEXT_FEATURES (bold, italic, link, ol, ul) can emit.
RICH_TAGS = {"p", "a", "b", "strong", "i", "em", "ol", "ul", "li", "br"}
INLINE_TAGS = {"br", "b", "strong", "i", "em"}
ATTRIBUTES = {"a": ["href"]}
TAB_IMAGE_WIDTH, TAB_IMAGE_HEIGHT = 1800, 1013
VANILLA_NOTIFICATION = {
    "information": "information",
    "success": "positive",
    "warning": "caution",
    "error": "negative",
}


def rich(html):
    """Rich text from the CMS, cut down to what its editor can produce."""
    return Markup(
        bleach.clean(
            str(html or ""), tags=RICH_TAGS, attributes=ATTRIBUTES, strip=True
        )
    )


def inline(text):
    """A one-line field that may carry <br> or emphasis, nothing else."""
    return Markup(bleach.clean(str(text or ""), tags=INLINE_TAGS, strip=True))


def img_attrs(url, alt, width, height):
    if not (width and height):
        return {"src": escape(url), "alt": escape(alt or "")}
    attrs = image_template(
        url=url,
        alt=alt or "",
        width=str(width),
        height=str(height),
        hi_def=True,
        output_mode="attrs",
    )
    return {name: escape(value) for name, value in attrs.items()}


def _button(text, url, suffix=""):
    if not text:
        return {}
    return {
        "content_html": escape(text) + Markup(suffix),
        "attrs": {"href": escape(url or "")},
    }


def cta_args(cta):
    cta = cta or {}
    secondary = _button(cta.get("secondary_text"), cta.get("secondary_url"))
    return {
        "primary": _button(cta.get("primary_text"), cta.get("primary_url")),
        "secondaries": [secondary] if secondary else [],
        "link": _button(
            cta.get("link_text"), cta.get("link_url"), "&nbsp;&rsaquo;"
        ),
    }


def _hero(value):
    blocks = []
    if value.get("signpost_image_url"):
        attrs = img_attrs(
            value["signpost_image_url"],
            value.get("signpost_image_alt"),
            value.get("signpost_image_width"),
            value.get("signpost_image_height"),
        )
        blocks.append({"type": "signpost_image", "item": {"attrs": attrs}})
    if value.get("description"):
        item = {"type": "html", "content": rich(value["description"])}
        blocks.append({"type": "description", "item": item})
    cta = cta_args(value.get("cta"))
    if any(cta.values()):
        blocks.append({"type": "cta-block", "item": cta})
    return {
        "title": inline(value.get("title")),
        "subtitle": escape(value.get("subtitle") or ""),
        "blocks": blocks,
    }


def _linked_logo_section(value):
    links = [
        {
            "href": escape(link.get("href") or ""),
            "text": inline(link.get("text")),
            "label": escape(link.get("label") or ""),
            "image_attrs": {
                "src": escape(link.get("image_url") or ""),
                "alt": escape(link.get("image_alt") or ""),
                "width": str(link.get("image_width") or ""),
                "height": str(link.get("image_height") or ""),
                "class": "",
            },
        }
        for link in value.get("links", [])
    ]
    return {"title": escape(value.get("title") or ""), "links": links}


def _logo_section(value):
    logos = [
        img_attrs(
            logo["image_url"],
            logo.get("alt"),
            logo.get("width"),
            logo.get("height"),
        )
        for logo in value.get("logos", [])
    ]
    return {
        "title": escape(value.get("title") or ""),
        "description": rich(value.get("description")),
        "blocks": [{"type": "logo-block", "item": {"logos": logos}}],
    }


def _tab(tab):
    content = Markup('<h3 class="p-heading--5">{}</h3>{}').format(
        tab.get("heading") or "", rich(tab.get("body"))
    )
    items = [
        {"type": "description", "item": {"type": "html", "content": content}}
    ]
    if tab.get("image_url"):
        attrs = img_attrs(
            tab["image_url"],
            tab.get("image_alt"),
            TAB_IMAGE_WIDTH,
            TAB_IMAGE_HEIGHT,
        )
        items.append({"type": "image", "item": {"attrs": attrs}})
    if tab.get("link_text"):
        link = _button(tab["link_text"], tab.get("link_url"), "&nbsp;&rsaquo;")
        items.append({"type": "cta-block", "item": {"link": link}})
    return {
        "tab_html": escape(tab.get("label") or ""),
        "type": "basic-section",
        "item": {"items": items},
    }


def _tab_section(value):
    return {
        "title": escape(value.get("title") or ""),
        "description": rich(value.get("description")),
        "tabs": [_tab(tab) for tab in value.get("tabs", [])],
    }


def _equal_heights_item(item):
    image_html = ""
    if item.get("image_url"):
        # image_template's default "html" output mode does not escape its
        # url/alt inputs, so escape them before they land in the HTML string.
        image_html = Markup(
            image_template(
                url=str(escape(item["image_url"])),
                alt=str(escape(item.get("image_alt") or "")),
                width="852",
                height="852",
                hi_def=True,
            )
        )
    return {
        "title_text": escape(item.get("title") or ""),
        "description_html": rich(item.get("description")),
        "image_html": image_html,
    }


def _equal_heights(value):
    return {
        "title": escape(value.get("title") or ""),
        "description": rich(value.get("description")),
        "cta": cta_args(value.get("cta")),
        "items": [_equal_heights_item(i) for i in value.get("items", [])],
    }


def _tiered_list(value):
    return {
        "description": rich(value.get("description")),
        "cta": cta_args(value.get("cta")),
        "items": [
            {
                "title": escape(item.get("title") or ""),
                "description": rich(item.get("description")),
            }
            for item in value.get("items", [])
        ],
    }


def _text_section(value):
    return {
        "heading": inline(value.get("heading")),
        "body": rich(value.get("body")),
    }


def _latest_blog(value):
    heading = value.get("heading") or "posts"
    slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
    return {
        "heading": escape(value.get("heading") or ""),
        "container_id": f"latest-blog-{slug}-articles",
        "template_id": f"latest-blog-{slug}-template",
    }


def _announcement(value):
    modifier = VANILLA_NOTIFICATION.get(
        value.get("criticality"), "information"
    )
    return {"modifier": modifier, "body": rich(value.get("body"))}


def _value_only(value):
    return {}


SHAPERS = {
    "hero": _hero,
    "linked_logo_section": _linked_logo_section,
    "logo_section": _logo_section,
    "tab_section": _tab_section,
    "equal_heights": _equal_heights,
    "tiered_list": _tiered_list,
    "link_list_section": _value_only,
    "highlight_list_section": _value_only,
    "text_section": _text_section,
    "latest_blog": _latest_blog,
    "announcement": _announcement,
    "data_list_section": _value_only,
}


def prepare_sections(body):
    sections = []
    for block in body or []:
        shaper = SHAPERS.get(block.get("type"))
        if not shaper:
            # A pattern the CMS knows and this renderer does not.
            continue
        value = block.get("value") or {}
        sections.append(
            {"type": block["type"], "value": value, "macro": shaper(value)}
        )
    return sections
