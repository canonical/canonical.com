import os

from playwright.sync_api import Page
from tests import webapp


def test_author_names(webapp, page: Page):
    page.goto("http://127.0.0.1:5000/careers")

    # Get number of "engineering" roles
    breakpoint()
    engineering_count = page.locator("#engineering-count").all_text_contents()
