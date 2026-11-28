import re
import unittest
from collections import Counter

import flask
from canonicalwebteam.markdown_response.converter import (
    convert_html_to_markdown,
)

from webapp.app import app, get_modal_form

WRAPPER_TEMPLATE = "knowledge/_base_knowledge_markdown.html"
ARTICLE_PATH = "/knowledge/data-and-ai-ml/test-article"
DATA_FORM = {"path": "/data", "modal_id": "data-modal"}


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


class TestGetModalForm(unittest.TestCase):
    def test_finds_form_from_relative_link(self):
        self.assertEqual(get_modal_form(["/data#get-in-touch"]), DATA_FORM)

    def test_finds_form_from_absolute_link(self):
        self.assertEqual(
            get_modal_form(["https://canonical.com/data/#get-in-touch"]),
            DATA_FORM,
        )

    def test_child_page_uses_parent_form(self):
        self.assertEqual(
            get_modal_form(["/data/services#get-in-touch"]), DATA_FORM
        )

    def test_finds_form_not_keyed_by_page_url(self):
        self.assertEqual(
            get_modal_form(
                [
                    "https://canonical.com/solutions/open-source-security"
                    "#get-in-touch"
                ]
            ),
            {
                "path": "/open-source-security",
                "modal_id": "secure-open-source-modal",
            },
        )

    def test_returns_first_link_with_modal_form(self):
        self.assertEqual(
            get_modal_form(
                [
                    "https://ubuntu.com/pro",
                    "/data#get-in-touch",
                    "/solutions/iot-and-devices#get-in-touch",
                ]
            ),
            DATA_FORM,
        )

    def test_ignores_links_without_modal_form(self):
        for url in [
            "/data",
            "#get-in-touch",
            "https://ubuntu.com/data#get-in-touch",
            "/not-a-page#get-in-touch",
            "/observability/contact-us#get-in-touch",
            "",
            None,
        ]:
            with self.subTest(url=url):
                self.assertIsNone(get_modal_form([url]))


class TestKnowledgeArticleForms(unittest.TestCase):
    cta = {
        "buttons": [
            {
                "text": "Get in touch",
                "url": "https://canonical.com/data#get-in-touch",
                "type": "button",
                "variant": "positive",
            },
            {"text": "Learn more", "url": "/data"},
        ]
    }

    def test_renders_linked_form_as_modal(self):
        html = render_article(cta=self.cta)

        self.assertIn(
            '<div class="p-modal u-display-none" id="data-modal">', html
        )
        return_url = re.search(r'name="returnURL"\s+value=(\S+)', html)
        self.assertEqual(
            return_url.group(1), f"{ARTICLE_PATH}#contact-form-success"
        )

    def test_form_link_opens_modal(self):
        html = render_article(cta=self.cta)

        self.assertIn(
            '<a href="https://canonical.com/data#get-in-touch" '
            'class="p-button p-button--positive js-invoke-modal" '
            'aria-controls="data-modal">Get in touch</a>',
            html,
        )
        self.assertIn('<a href="/data">Learn more</a>', html)

    def test_only_first_linked_form_opens_in_place(self):
        cta = {
            "buttons": [
                *self.cta["buttons"],
                {
                    "text": "IoT",
                    "url": "/solutions/iot-and-devices#get-in-touch",
                },
            ]
        }
        html = render_article(cta=cta)

        self.assertEqual(html.count('class="p-modal '), 1)
        self.assertIn(
            '<a href="/solutions/iot-and-devices#get-in-touch">IoT</a>', html
        )

    def test_no_form_link_leaves_page_unchanged(self):
        cta = {"buttons": [{"text": "Pro", "url": "https://ubuntu.com/pro"}]}

        for context in [{"cta": cta}, {}]:
            with self.subTest(context=context):
                html = render_article(**context)

                self.assertNotIn('class="p-modal', html)
                self.assertNotIn("js-invoke-modal", html)

        self.assertIn(
            '<a href="/contact-us" class="p-button--positive">Contact us</a>',
            render_article(),
        )

    def test_modal_left_out_of_markdown(self):
        html = render_article(cta=self.cta)

        self.assertIn("within one working day", html)
        self.assertNotIn(
            "within one working day", convert_html_to_markdown(html)
        )

    def test_modal_ids_are_unique(self):
        """
        The modal's fields mustn't share IDs with the rest of the article,
        such as the newsletter signup form. "company" is excluded because
        every modal form clashes with the navigation's company dropdown.
        """
        ids = Counter(
            re.findall(r'\sid="([^"]+)"', render_article(cta=self.cta))
        )
        duplicates = {id for id, count in ids.items() if count > 1}

        self.assertEqual(duplicates - {"company"}, set())


if __name__ == "__main__":
    unittest.main()
