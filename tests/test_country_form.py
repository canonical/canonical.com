import unittest
from html.parser import HTMLParser
from pathlib import Path


class CountryOptionCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.options = {}
        self.current_value = None

    def handle_starttag(self, tag, attrs):
        if tag == "option":
            self.current_value = dict(attrs).get("value")

    def handle_data(self, data):
        if self.current_value:
            self.options[self.current_value] = data

    def handle_endtag(self, tag):
        if tag == "option":
            self.current_value = None


class TestCountryForm(unittest.TestCase):
    def test_uses_current_country_names(self):
        country_template = (
            Path(__file__).parents[1]
            / "templates"
            / "shared"
            / "forms"
            / "_country.html"
        )
        parser = CountryOptionCollector()
        parser.feed(country_template.read_text())

        self.assertEqual(parser.options["MK"], "North Macedonia")
        self.assertEqual(parser.options["SZ"], "Eswatini")


if __name__ == "__main__":
    unittest.main()
