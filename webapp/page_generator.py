import json
from pathlib import Path
import subprocess
from flask import current_app
from abc import ABC, abstractmethod
from typing import List, Optional, Protocol
from jsonschema import validate, ValidationError


class FileWriter(Protocol):
    """Interface for file writing operations."""

    def write(self, path: Path, content: str) -> str:
        """Write content to file and return the relative path."""
        ...


class HTMLFormatter(Protocol):
    """Interface for HTML formatting operations."""

    def format(self, html_content: str) -> str:
        """Format HTML content and return the result."""
        ...


class HTMLBuilder(Protocol):
    """Interface for HTML building operations."""

    def init_html(self) -> str:
        """Return the initial HTML structure."""
        ...

    def finish_html(self) -> str:
        """Return the closing HTML structure."""
        ...


class ContentBuilder(Protocol):
    """Interface for content building operations."""

    def clear(self) -> None:
        """Clear the content builder."""
        ...

    def add_imports(self, patterns: List["Pattern"]) -> None:
        """Collect and add import statements from patterns."""
        ...

    def add_content_start(self) -> None:
        """Add the content block start."""
        ...

    def add_patterns(self, patterns: List["Pattern"]) -> None:
        """Process patterns and add their HTML."""
        ...

    def build(self) -> str:
        """Build and return the complete HTML content."""
        ...


class PatternFactory:
    """Factory for creating pattern instances based on type."""

    def __init__(self):
        self._patterns = {
            "hero": HeroSection,
            "basic": BasicSection,
            "cta": CTASection,
            "resources": ResourcesSection,
        }

    def register_pattern(self, pattern_type: str, pattern_class: type):
        self._patterns[pattern_type] = pattern_class

    def create(
        self, pattern_type: str, pattern_data: dict
    ) -> Optional["Pattern"]:
        """Create a pattern instance based on type."""
        pattern_class = self._patterns.get(pattern_type)
        if pattern_class:
            return pattern_class(pattern_data)
        return None


class HTMLContentBuilder:
    """Responsible for building HTML content from patterns."""

    def __init__(self):
        self.content_parts = []

    def add_imports(self, patterns: List["Pattern"]) -> None:
        """Collect and add import statements from patterns."""
        imports = set()
        for pattern in patterns:
            import_statement = pattern.write_import()
            if import_statement:
                imports.add(import_statement.strip())

        for import_stmt in imports:
            self.content_parts.append(f"\n{import_stmt}\n")

    def add_content_start(self) -> None:
        """Add the content block start."""
        self.content_parts.append(
            """
            {% block content %}
        """
        )

    def add_patterns(self, patterns: List["Pattern"]) -> None:
        """Process patterns and add their HTML."""
        for pattern in patterns:
            pattern.process_pattern()
            self.content_parts.append(pattern.pattern_html)

    def build(self) -> str:
        """Build and return the complete HTML content."""
        return "".join(self.content_parts)

    def clear(self) -> None:
        """Clear the content builder."""
        self.content_parts = []


class TemplateFileWriter:
    """Responsible for writing template files to disk."""

    def __init__(self, base_path: Path):
        self.base_path = base_path

    def write(self, path: Path, content: str) -> str:
        """Write content to file and return relative path."""
        full_path = self.base_path / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(full_path.with_suffix("")).split("templates/")[-1]


class PageGenerator:
    """Orchestrates the page generation process."""

    def __init__(
        self,
        data: dict,
        pattern_factory: PatternFactory,
        html_builder: HTMLBuilder,
        content_builder: ContentBuilder,
        formatter: HTMLFormatter,
        file_writer: FileWriter,
    ):
        self.data = data
        self.pattern_factory = pattern_factory
        self.html_builder = html_builder
        self.content_builder = content_builder
        self.formatter = formatter
        self.file_writer = file_writer
        self.patterns = []

    def _create_patterns(self) -> None:
        """Create pattern instances from data."""
        for pattern in self.data.get("patterns", []):
            pattern_type = pattern.get("name")
            pattern_data = pattern.get("data", {})
            pattern_instance = self.pattern_factory.create(
                pattern_type, pattern_data
            )
            if pattern_instance:
                self.patterns.append(pattern_instance)

    def _build_content(self) -> str:
        """Build the HTML content."""
        self.content_builder.clear()
        self.content_builder.add_imports(self.patterns)
        self.content_builder.add_content_start()
        self.content_builder.add_patterns(self.patterns)
        return self.content_builder.build()

    def _get_output_path(self) -> Path:
        """Get the output file path."""
        p_path = self.data.get("page_path", "").lstrip("/")
        p_name = self.data.get("page_name", "").lstrip("/")
        return Path(p_path) / f"{p_name}.html"

    def generate(self) -> str:
        """Generate the page and return the relative path."""
        # Create patterns
        self._create_patterns()

        # validate patterns payload
        for pattern in self.patterns:
            is_valid, error_msg = pattern.validate_payload()
            if not is_valid:
                raise ValueError(f"Pattern validation failed: {error_msg}")

        # Build HTML
        html_parts = [
            self.html_builder.init_html(),
            self._build_content(),
            self.html_builder.finish_html(),
        ]
        html_content = "".join(html_parts)

        # Format HTML
        formatted_html = self.formatter.format(html_content)

        # Write to file
        output_path = self._get_output_path()
        return self.file_writer.write(output_path, formatted_html)


class HTMLGenerator:
    """Concrete implementation of HTML structure generation."""

    def init_html(self) -> str:
        return """
            {% extends 'base_index.html' %}

            {% block body_class %}
                is-paper
            {% endblock body_class %}
        """

    def finish_html(self) -> str:
        return """
            {% endblock %}
        """


class DjlintFormatter:
    """Concrete implementation of HTML formatting using djlint."""

    def format(self, html_content: str) -> str:
        try:
            result = subprocess.run(
                ["djlint", "-", "--reformat"],
                input=html_content,
                text=True,
                capture_output=True,
                check=True,
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # If djlint fails or is not installed, return the original content
            current_app.logger.warning(f"djlint formatting failed: {e}")
            return html_content


class Pattern(ABC):
    def __init__(self, data):
        self.data = data
        self.pattern_html = ""

    @abstractmethod
    def process_pattern(self):
        pass

    @abstractmethod
    def write_import(self):
        """Return the import statement for this pattern,
        or None if not needed."""
        pass


class HeroSection(Pattern):
    def __init__(self, data):
        super().__init__(data)

    def process_pattern(self):
        params_list = []

        for key, value in self.data.items():
            if isinstance(value, str):
                # Wrap strings in double quotes
                params_list.append(f'{key}="{value}"')
            elif isinstance(value, bool):
                # Lowercase booleans for Jinja
                params_list.append(f"{key}={str(value).lower()}")
            else:
                # For dicts, lists, numbers: convert to JSON
                # so Jinja sees a valid object literal
                params_list.append(f"{key}={json.dumps(value)}")

        # Join all parameters with commas
        params_str = ",\n    ".join(params_list)

        self.pattern_html += f"""
            {{% call(slot) vf_hero(
                {params_str}
            ) -%}}

            {{% endcall -%}}
        """

    def write_import(self):
        return '{% from "_macros/vf_hero.jinja" import vf_hero %}'

    def validate_payload(self):
        # load json schema for hero
        with open(
            Path(current_app.root_path).resolve().parent
            / "static/json/page-generator/schemas/hero.json",
            "r",
        ) as f:
            HERO_SCHEMA = json.load(f)

        try:
            # This matches the payload
            # against your schema including definitions
            print(f"Validating HeroSection with data: {self.data}")
            validate(instance=self.data, schema=HERO_SCHEMA)
            return True, None
        except ValidationError as e:
            # Returns a readable error message
            # and the path to the failing field
            error_path = " -> ".join([str(p) for p in e.path])
            return False, f"Validation Error at [{error_path}]: {e.message}"


class BasicSection(Pattern):
    def __init__(self, data):
        super().__init__(data)

    def process_pattern(self):
        # TODO: Implement basic section pattern
        pass

    def write_import(self):
        return None


class CTASection(Pattern):
    def __init__(self, data):
        super().__init__(data)

    def process_pattern(self):
        # TODO: Implement CTA section pattern
        pass

    def write_import(self):
        return None


class ResourcesSection(Pattern):
    def __init__(self, data):
        super().__init__(data)

    def process_pattern(self):
        # TODO: Implement resources section pattern
        pass

    def write_import(self):
        return None


def create_page_generator(data: dict) -> PageGenerator:
    """
    Factory function to create a fully configured PageGenerator instance.
    """
    BASE_DIR = Path(current_app.root_path).resolve().parent
    templates_path = BASE_DIR / "templates"

    pattern_factory = PatternFactory()
    html_builder = HTMLGenerator()
    content_builder = HTMLContentBuilder()
    formatter = DjlintFormatter()
    file_writer = TemplateFileWriter(templates_path)
    #test

    return PageGenerator(
        data=data,
        pattern_factory=pattern_factory,
        html_builder=html_builder,
        content_builder=content_builder,
        formatter=formatter,
        file_writer=file_writer,
    )
