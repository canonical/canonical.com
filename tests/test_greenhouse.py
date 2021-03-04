import unittest
from webapp.greenhouse import Department


class TestGreenhouseAPI(unittest.TestCase):
    def test_parse_feed_department_not_matched(self):
        department = "foo"
        parsed_department = Department(department)
        self.assertEqual(parsed_department.slug, department)

    def test_parse_feed_department_matched(self):
        department = "cloud engineering"
        parsed_department = Department(department)
        self.assertEqual(parsed_department.slug, "engineering")


if __name__ == "__main__":
    unittest.main()
