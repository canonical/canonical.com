import json
from pathlib import Path
from flask import current_app


class SchemaLoader:
    """Loads and caches JSON schemas from files."""

    _cache = {}
    _ui_cache = {}

    @classmethod
    def _schemas_dir(cls) -> Path:
        return (
            Path(current_app.root_path).resolve().parent
            / "static/json/page-generator/schemas"
        )

    @classmethod
    def get_schema(cls, schema_name: str) -> dict:
        """Load schema from file if not already cached."""
        if schema_name not in cls._cache:
            schema_path = cls._schemas_dir() / f"{schema_name}.json"
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

    @classmethod
    def get_ui_schema(cls, schema_name: str) -> dict:
        """Load UI schema from file if not already cached."""
        if schema_name not in cls._ui_cache:
            schema_path = cls._schemas_dir() / f"{schema_name}.ui.json"
            try:
                with open(schema_path, "r", encoding="utf-8") as f:
                    cls._ui_cache[schema_name] = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"UI schema file not found: {schema_path}"
                )
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"UI schema file '{schema_path}' "
                    f"contains invalid JSON: {e}"
                )
            except OSError as e:
                raise OSError(
                    f"Unable to read UI schema file '{schema_path}': {e}"
                )
        return cls._ui_cache[schema_name]

    @classmethod
    def get_all_schemas(cls) -> dict:
        """Return all pattern schemas and their UI definitions."""
        schemas = {}

        for schema_path in sorted(cls._schemas_dir().glob("*.json")):
            if schema_path.name.endswith(".ui.json"):
                continue

            schema_name = schema_path.stem
            ui_schema = cls.get_ui_schema(schema_name)
            schemas[schema_name] = {
                "schema": cls.get_schema(schema_name),
                "uiSchema": ui_schema,
                "label": ui_schema.get("ui:label", schema_name),
                "description": ui_schema.get("ui:description", ""),
            }

        return schemas
