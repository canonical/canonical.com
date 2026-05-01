import re

import flask

from .schema import SchemaLoader

_SAFE_NAME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")


def page_generator_error(
    message: str, field: str = "payload", status_code: int = 400
):
    return (
        flask.jsonify({"errors": [{"field": field, "message": message}]}),
        status_code,
    )


def build_page_url(payload: dict) -> str:
    page_path = str(payload.get("page_path", "")).strip("/")
    page_name = str(payload.get("page_name", "")).strip("/")
    return f"/{'/'.join([part for part in [page_path, page_name] if part])}"


def normalise_page_generator_sections(sections) -> list:
    if not isinstance(sections, list):
        raise ValueError("'sections' must be a list")

    normalised_sections = []
    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            raise ValueError(f"Section at index {index} must be an object")

        name = section.get("name") or section.get("pattern")
        if not name or not isinstance(name, str):
            raise ValueError(
                f"Section at index {index} must include a pattern name"
            )

        if not _SAFE_NAME_RE.match(name):
            raise ValueError(
                "Invalid section name at index" f" {index}: '{name}'"
            )

        try:
            SchemaLoader.get_schema(name)
        except (FileNotFoundError, ValueError, OSError):
            raise ValueError(f"Unknown or invalid schema for section '{name}'")

        data = section.get("data")
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise ValueError(f"Section data for '{name}' must be an object")

        normalised_sections.append({"name": name, "data": data})

    return normalised_sections


def normalise_page_generator_payload(payload: dict) -> dict:
    sections = payload.get("sections")
    patterns = payload.get("patterns")

    if sections is not None and patterns is not None:
        raise ValueError("Provide either 'sections' or 'patterns', not both")

    source = sections if sections is not None else patterns
    if source is None:
        source = []

    normalised_patterns = normalise_page_generator_sections(source)

    page_name = payload.get("page_name", "preview")
    page_path = payload.get("page_path", "/")

    if not isinstance(page_name, str) or not page_name.strip():
        raise ValueError("'page_name' must be a non-empty string")
    if not isinstance(page_path, str):
        raise ValueError("'page_path' must be a string")

    if ".." in page_name or "/" in page_name or "\\" in page_name:
        raise ValueError(
            "'page_name' must not contain" " path separators or '..'"
        )
    if ".." in page_path:
        raise ValueError("'page_path' must not contain '..'")

    return {
        "page_name": page_name,
        "page_path": page_path,
        "patterns": normalised_patterns,
    }
