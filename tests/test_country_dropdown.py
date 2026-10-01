import unittest
from pathlib import Path


class TestCountryDropdown(unittest.TestCase):
    def test_uses_current_country_names(self):
        template_path = (
            Path(__file__).resolve().parents[1]
            / "templates/shared/forms/_country.html"
        )
        template = template_path.read_text()

        self.assertIn('<option value="MK">North Macedonia</option>', template)
        self.assertIn('<option value="SZ">Eswatini</option>', template)
        self.assertNotIn(
            "Macedonia (the former Yugoslav Republic of)", template
        )
        self.assertNotIn(">Swaziland</option>", template)


if __name__ == "__main__":
    unittest.main()
