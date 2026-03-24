import json
from pathlib import Path
from flask import current_app


class SchemaLoader:
    """Loads and caches JSON schemas from files."""

    _cache = {}

    @classmethod
    def get_schema(cls, schema_name: str) -> dict:
        """Load schema from file if not already cached."""
        if schema_name not in cls._cache:
            schema_path = (
                Path(current_app.root_path).resolve().parent
                / f"static/json/page-generator/schemas/{schema_name}.json"
            )
            try:
                with open(schema_path, "r") as f:
                    cls._cache[schema_name] = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Schema file not found: {schema_path}"
                )
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Schema file '{schema_path}' contains invalid JSON: {e}"
                )
            except OSError as e:
                raise OSError(
                    f"Unable to read schema file '{schema_path}': {e}"
                )
        return cls._cache[schema_name]
