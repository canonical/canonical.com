import flask

from .schema import SchemaLoader


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
    page_path = payload.get("page_path", "/page-generator/preview")

    if not isinstance(page_name, str) or not page_name.strip():
        raise ValueError("'page_name' must be a non-empty string")
    if not isinstance(page_path, str) or not page_path.strip():
        raise ValueError("'page_path' must be a non-empty string")

    return {
        "page_name": page_name,
        "page_path": page_path,
        "patterns": normalised_patterns,
    }
