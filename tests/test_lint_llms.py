import unittest

from scripts import lint_llms


class TestFindProducts(unittest.TestCase):
    def test_detects_product_names(self):
        self.assertEqual(lint_llms.find_products("The Juju CLI"), {"juju"})
        self.assertEqual(
            lint_llms.find_products("Ubuntu Server docs"), {"ubuntu server"}
        )
        # Bare "ubuntu" is intentionally not a product token.
        self.assertEqual(lint_llms.find_products("Ubuntu desktop"), set())
        self.assertEqual(lint_llms.find_products(""), set())


class TestLintConfig(unittest.TestCase):
    def _extra(self, links):
        return {"extra": [{"heading": "Documentation", "links": links}]}

    def test_valid_config_passes(self):
        config = self._extra(
            [
                {
                    "title": "Juju",
                    "url": "https://canonical.com/juju/docs",
                    "description": "Operate apps with Juju.",
                }
            ]
        )
        errors, warnings = lint_llms.lint_config(config)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_missing_description_is_error(self):
        config = self._extra(
            [{"title": "Juju", "url": "https://canonical.com/juju"}]
        )
        errors, _ = lint_llms.lint_config(config)
        self.assertEqual(len(errors), 1)
        self.assertIn("missing description", errors[0])

    def test_missing_title_or_url_is_error(self):
        config = self._extra([{"title": "Juju", "description": "d"}])
        errors, _ = lint_llms.lint_config(config)
        self.assertIn("needs both a title and a url", errors[0])

    def test_duplicate_description_is_error(self):
        config = self._extra(
            [
                {
                    "title": "A",
                    "url": "https://x.com/a",
                    "description": "Same.",
                },
                {
                    "title": "B",
                    "url": "https://x.com/b",
                    "description": "Same.",
                },
            ]
        )
        errors, _ = lint_llms.lint_config(config)
        self.assertEqual(len(errors), 1)
        self.assertIn("duplicated", errors[0])

    def test_wrong_product_is_warning(self):
        # The exact slip Massi flagged: a Juju link described as Ubuntu Server.
        config = self._extra(
            [
                {
                    "title": "Juju",
                    "url": "https://canonical.com/juju/docs/juju-cli/page",
                    "description": "Official Ubuntu Server documentation.",
                }
            ]
        )
        errors, warnings = lint_llms.lint_config(config)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("wrong description", warnings[0])

    def test_noop_override_is_warning(self):
        config = {"overrides": {"/x": {"something": "ignored"}}}
        _, warnings = lint_llms.lint_config(config)
        self.assertEqual(len(warnings), 1)
        self.assertIn("/x", warnings[0])

    def test_shipped_config_is_clean(self):
        import yaml

        config = yaml.safe_load(lint_llms.CONFIG_PATH.read_text()) or {}
        errors, warnings = lint_llms.lint_config(config)
        self.assertEqual(errors, [], f"shipped llms.yaml has errors: {errors}")
        self.assertEqual(
            warnings, [], f"shipped llms.yaml has warnings: {warnings}"
        )


if __name__ == "__main__":
    unittest.main()
