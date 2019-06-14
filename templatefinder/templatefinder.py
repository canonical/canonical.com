import os

import bleach

from flask import abort, current_app, render_template, request
from flask.views import View
from frontmatter import loads as load_frontmatter_from_markdown
from jinja2.exceptions import TemplateNotFound
from mistune import Markdown


class TemplateFinder(View):
    """
    A TemplateView that guesses the template name based on the
    url path
    """

    def __init__(self):
        self.markdown_parser = Markdown(
            parse_block_html=True, parse_inline_html=True
        )

    def dispatch_request(self, *args, **kwargs):
        """
        This is called when TemplateFinder is run as a view
        It tries to find the template for the request path
        and then passes that template name to TemplateView to render
        """
        path = request.path.lstrip("/")
        matching_template = self._get_template(path)

        if not matching_template:
            abort(404, f"Can't find page for: {path}")

        if matching_template[-2:] == "md":
            with open(
                f"{current_app.template_folder}/{matching_template}"
            ) as f:
                file_content = f.read()
                parsed_file = load_frontmatter_from_markdown(file_content)
                wrapper_template = parsed_file.metadata.get("wrapper_template")

                if not wrapper_template or not os.path.isfile(
                    current_app.template_folder + "/" + wrapper_template
                ):
                    abort(404, f"Can't find page for: {path}")

                context = parsed_file.metadata.get("context", {})
                return self._render_markdown(
                    parsed_file.content, wrapper_template, context
                )

        return render_template(matching_template, **self._get_context())

    def _get_context(self):
        context = {}
        clean_path = request.path.strip("/")
        for index, path in enumerate(clean_path.split("/")):
            context["level_" + str(index + 1)] = path
        return context

    def _get_template(self, url_path):
        """
        Given a basic path, find an HTML or Markdown file
        """

        # Try to match HTML or Markdown files
        if self._template_exists(url_path + ".html"):
            return url_path + ".html"
        elif self._template_exists(os.path.join(url_path, "index.html")):
            return os.path.join(url_path, "index.html")
        elif self._template_exists(url_path + ".md"):
            return url_path + ".md"
        elif self._template_exists(os.path.join(url_path, "index.md")):
            return os.path.join(url_path, "index.md")

        return None

    def _template_exists(self, path):
        """
        Check if a template exists
        without raising an exception
        """
        loader = current_app.jinja_loader
        try:
            loader.get_source({}, template=path)
        except TemplateNotFound:
            return False

        return True

    def _render_markdown(self, markdown, wrapper_file, context={}):
        """
        :param markdown: Markdown to be rendered
        :param wrapper_file: The wrapper for the Markdown content
        :param context: Optional preexisting context
        """

        clean_markdown = bleach.clean(markdown)
        rendered_markdown = self.markdown_parser(clean_markdown)

        context = {"content": rendered_markdown}

        return render_template(wrapper_file, **context)
