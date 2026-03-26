"""Flask extension to serve HTML pages as Markdown via ?format=md."""

import logging

from flask import request

from .converter import (
    DEFAULT_CONTENT_SELECTOR,
    DEFAULT_STRIP_CLASSES,
    DEFAULT_STRIP_ELEMENTS,
    convert_html_to_markdown,
)
from .frontmatter import extract_frontmatter

logger = logging.getLogger(__name__)


class MarkdownResponse:
    """Flask extension that adds ?format=md support to all HTML responses.

    Usage:
        app = Flask(__name__)
        MarkdownResponse(app)

    Or with the application factory pattern:
        md = MarkdownResponse()
        md.init_app(app)

    Configuration via constructor kwargs:
        MarkdownResponse(app,
            content_selector="#main-content",
            strip_elements=["script", "style", "nav", "noscript"],
            strip_classes=["u-hide", "u-off-screen"],
            query_param="format",
            query_value="md",
        )
    """

    def __init__(self, app=None, **kwargs):
        self.content_selector = kwargs.get(
            "content_selector", DEFAULT_CONTENT_SELECTOR
        )
        self.strip_elements = kwargs.get(
            "strip_elements", DEFAULT_STRIP_ELEMENTS
        )
        self.strip_classes = kwargs.get("strip_classes", DEFAULT_STRIP_CLASSES)
        self.query_param = kwargs.get("query_param", "format")
        self.query_value = kwargs.get("query_value", "md")

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register the after_request handler on the Flask app."""
        app.extensions["markdown_response"] = self
        app.after_request(self._handle_markdown_request)

    def _handle_markdown_request(self, response):
        """Convert HTML responses to Markdown when ?format=md is present."""
        if request.args.get(self.query_param) != self.query_value:
            return response

        if "text/html" not in response.content_type:
            return response

        if response.status_code != 200:
            return response

        try:
            html = response.get_data(as_text=True)

            frontmatter = extract_frontmatter(html)
            markdown_body = convert_html_to_markdown(
                html,
                content_selector=self.content_selector,
                strip_elements=self.strip_elements,
                strip_classes=self.strip_classes,
            )

            markdown_output = frontmatter + "\n" + markdown_body
            response.set_data(markdown_output)
            response.content_type = "text/markdown; charset=utf-8"
        except Exception:
            logger.exception("Failed to convert response to Markdown")

        return response
