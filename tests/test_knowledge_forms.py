import re
import unittest
from pathlib import Path

import flask
import frontmatter

from webapp.app import app, form_loader, get_form_modal_id

KNOWLEDGE_DIR = Path(app.root_path).parent / "templates" / "knowledge"
WRAPPER_TEMPLATE = "knowledge/_base_knowledge_markdown.html"
ARTICLE_PATH = "/knowledge/data-and-ai-ml/test-article"


def render_article(**context):
    defaults = {
        "title": "Test article",
        "description": "Test description",
        "category": "Data and AI/ML",
        "breadcrumb": "Test article",
        "hero_title": "Test article",
        "content": "<p>Body</p>",
        "blog": {},
    }
    defaults.update(context)
    with app.test_request_context(ARTICLE_PATH):
        return flask.render_template(WRAPPER_TEMPLATE, **defaults)


class TestGetFormModalId(unittest.TestCase):
    def test_returns_modal_id_for_form(self):
        self.assertEqual(get_form_modal_id("/data"), "data-modal")

    def test_returns_parent_modal_id_for_child_path(self):
        self.assertEqual(get_form_modal_id("/data/services"), "data-modal")

    def test_returns_none_for_unknown_form(self):
        self.assertIsNone(get_form_modal_id("/not-a-form"))


class TestKnowledgeArticleForms(unittest.TestCase):
    cta = {
        "buttons": [
            {
                "text": "Get in touch",
                "url": "#get-in-touch",
                "type": "button",
                "variant": "positive",
            },
            {"text": "Learn more", "url": "/data"},
        ]
    }

    def test_renders_form_as_modal_on_article(self):
        html = render_article(form="/data", cta=self.cta)

        self.assertIn(
            '<div class="p-modal u-display-none" id="data-modal">', html
        )
        return_url = re.search(r'name="returnURL"\s+value=(\S+)', html)
        self.assertEqual(
            return_url.group(1), f"{ARTICLE_PATH}#contact-form-success"
        )

    def test_get_in_touch_button_opens_modal(self):
        html = render_article(form="/data", cta=self.cta)

        self.assertIn(
            '<a href="#get-in-touch" '
            'class="p-button p-button--positive js-invoke-modal" '
            'aria-controls="data-modal">Get in touch</a>',
            html,
        )
        self.assertIn('<a href="/data">Learn more</a>', html)

    def test_default_cta_opens_modal(self):
        html = render_article(form="/data")

        self.assertIn('aria-controls="data-modal">Contact us</a>', html)
        self.assertNotIn(
            '<a href="/contact-us" class="p-button--positive">Contact us</a>',
            html,
        )

    def test_no_form_leaves_page_unchanged(self):
        html = render_article(cta=self.cta)

        self.assertNotIn('class="p-modal', html)
        self.assertNotIn("js-invoke-modal", html)
        self.assertIn('<a href="#get-in-touch" class="p-button', html)

    def test_article_forms_exist(self):
        """
        Every knowledge article's `form` must be the top-level key of a
        modal form in a form-data.json. Child paths are rejected because
        their submissions redirect to the parent page, not the article.
        """
        for article in KNOWLEDGE_DIR.rglob("*.md"):
            context = frontmatter.load(article).metadata.get("context", {})
            form_path = (context or {}).get("form")
            if not form_path:
                continue

            with self.subTest(article=article.relative_to(KNOWLEDGE_DIR)):
                form_info = form_loader.form_metadata.get(form_path)
                self.assertIsNotNone(
                    form_info, f"No form registered at {form_path}"
                )
                self.assertFalse(
                    form_info.get("is_child"),
                    f"{form_path} is a child path; use its parent form",
                )
                self.assertIsNotNone(
                    get_form_modal_id(form_path),
                    f"{form_path} has no modalId",
                )


if __name__ == "__main__":
    unittest.main()
