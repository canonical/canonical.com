#!/usr/bin/env python3
"""Lint llms.yaml — the docs-team-owned config for /llms.txt.

Manual entries (curated ``extra`` links and ``overrides``) are the ones that
drift, so this catches the common failure modes:

  * a curated link with no description (errors — the description is the value
    over a plain sitemap);
  * the same description reused for different links (errors — usually a
    copy-paste slip);
  * a description that names a different product than the link (warns — a
    heuristic for "wrong" descriptions a checker can't fully verify).

Errors fail the build; warnings are printed but do not. Run via
``yarn lint-llms`` or ``python3 scripts/lint_llms.py``.
"""

import re
import sys
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "llms.yaml"

# Product/section names used to spot a description about the wrong thing.
# Multi-word "ubuntu *" entries are listed instead of bare "ubuntu" so that
# legitimately Ubuntu-related copy does not trip the heuristic.
PRODUCTS = [
    "ubuntu server",
    "ubuntu pro",
    "ubuntu core",
    "juju",
    "jaas",
    "maas",
    "microk8s",
    "kubernetes",
    "kubeflow",
    "ceph",
    "lxd",
    "openstack",
    "anbox",
    "multipass",
    "dqlite",
    "landscape",
    "charmhub",
    "snapcraft",
    "mir",
]


def find_products(text):
    """Return the set of known product names mentioned in *text*."""
    text = (text or "").lower()
    return {p for p in PRODUCTS if re.search(rf"\b{re.escape(p)}\b", text)}


def _iter_links(config):
    """Yield (label, title, url, description) for every curated extra link."""
    for section in config.get("extra") or []:
        heading = (section.get("heading") or "?").strip()
        for link in section.get("links") or []:
            title = (link.get("title") or "").strip()
            label = f"extra[{heading}] -> {title or link.get('url') or '?'}"
            yield (
                label,
                title,
                (link.get("url") or "").strip(),
                (link.get("description") or "").strip(),
            )


def lint_config(config):
    """Return (errors, warnings) for a parsed llms.yaml config dict."""
    errors = []
    warnings = []
    seen_descriptions = {}

    for label, title, url, description in _iter_links(config):
        if not title or not url:
            errors.append(f"{label}: link needs both a title and a url")
            continue
        if not description:
            errors.append(f"{label}: missing description")
            continue

        key = description.lower()
        if key in seen_descriptions:
            errors.append(
                f"{label}: description duplicated from "
                f"'{seen_descriptions[key]}'"
            )
        else:
            seen_descriptions[key] = label

        link_products = find_products(f"{title} {url}")
        desc_products = find_products(description)
        if link_products and desc_products.isdisjoint(link_products):
            warnings.append(
                f"{label}: description mentions "
                f"{sorted(desc_products)} but the link is about "
                f"{sorted(link_products)} — wrong description?"
            )

    # Overrides should actually change something.
    overrides = config.get("overrides") or {}
    for path, override in overrides.items():
        if not isinstance(override, dict) or not (
            override.get("title")
            or override.get("description")
            or override.get("exclude")
        ):
            warnings.append(
                f"overrides[{path}]: no title, description or exclude set"
            )

    return errors, warnings


def main():
    if not CONFIG_PATH.exists():
        print(f"llms lint: {CONFIG_PATH} not found, nothing to check")
        return 0

    try:
        config = yaml.safe_load(CONFIG_PATH.read_text()) or {}
    except yaml.YAMLError as error:
        print(f"llms lint: failed to parse {CONFIG_PATH.name}: {error}")
        return 1

    errors, warnings = lint_config(config)

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")

    if errors:
        print(f"\nllms lint: {len(errors)} error(s) in {CONFIG_PATH.name}")
        return 1

    print(
        f"llms lint: {CONFIG_PATH.name} OK"
        + (f" ({len(warnings)} warning(s))" if warnings else "")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
