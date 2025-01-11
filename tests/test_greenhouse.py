import unittest
from webapp.greenhouse import Department


class TestGreenhouseAPI(unittest.TestCase):
    def test_parse_feed_department_not_matched(self):
        department = "foo"
        parsed_department = Department(department)
        self.assertEqual(parsed_department.slug, department)

    def test_parse_feed_department_matched(self):
        # Check '&' and ' ' get replaced in slugs
        web_and_design = Department("Web & Design")
        self.assertEqual(web_and_design.slug, "web-and-design")

        # Check department renames are happening
        techops = Department("Techops")
        self.assertEqual(techops.slug, "support-engineering")


if __name__ == "__main__":
    unittest.main()
