import unittest

from webapp.app import app


class TestCountryDropdown(unittest.TestCase):
    def test_uses_current_country_names(self):
        rendered = app.jinja_env.get_template(
            "shared/forms/_country.html"
        ).render()

        self.assertIn('<option value="MK">North Macedonia</option>', rendered)
        self.assertIn('<option value="SZ">Eswatini</option>', rendered)
        self.assertNotIn("Macedonia (the former Yugoslav Republic of)", rendered)
        self.assertNotIn(">Swaziland</option>", rendered)


if __name__ == "__main__":
    unittest.main()
