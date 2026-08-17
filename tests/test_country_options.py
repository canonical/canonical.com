import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class TestCountryOptionLabels(unittest.TestCase):
    def test_outdated_country_labels_removed_from_contact_templates(self):
        template_paths = [
            REPO_ROOT / "templates/shared/forms/_country.html",
            REPO_ROOT / "templates/partners/become-a-partner.html",
            REPO_ROOT / "templates/legal/terms-and-policies/contact-us.md",
            REPO_ROOT / "templates/legal/confidentiality-agreement.md",
        ]

        outdated_label_patterns = [
            r">\s*Macedonia \(the former Yugoslav Republic of\)\s*<",
            r">\s*Swaziland\s*<",
        ]

        for template_path in template_paths:
            with self.subTest(template=template_path.relative_to(REPO_ROOT)):
                template = template_path.read_text()

                for label_pattern in outdated_label_patterns:
                    self.assertNotRegex(template, label_pattern)

    def test_updated_country_labels_present_in_dropdown_templates(self):
        expected_labels_by_template = {
            REPO_ROOT
            / "templates/shared/forms/_country.html": [
                "North Macedonia",
                "Eswatini",
            ],
            REPO_ROOT / "templates/partners/become-a-partner.html": [
                "North Macedonia",
                "Eswatini",
            ],
            REPO_ROOT / "templates/legal/terms-and-policies/contact-us.md": [
                "Eswatini",
            ],
            REPO_ROOT / "templates/legal/confidentiality-agreement.md": [
                "Eswatini",
            ],
        }

        for template_path, expected_labels in expected_labels_by_template.items():
            with self.subTest(template=template_path.relative_to(REPO_ROOT)):
                template = template_path.read_text()

                for label in expected_labels:
                    self.assertRegex(template, rf">\s*{re.escape(label)}\s*<")
