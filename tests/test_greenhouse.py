import unittest
from webapp.greenhouse import _parse_feed_department


class TestGreenhouseAPI(unittest.TestCase):
    def test_parse_feed_department_not_matched(self):
        department = "foo"
        parsed_department = _parse_feed_department(department)
        self.assertEqual(parsed_department, department)

    def test_parse_feed_department_matched(self):
        department = "cloud engineering"
        parsed_department = _parse_feed_department(department)
        self.assertEqual(parsed_department, "engineering")


if __name__ == "__main__":
    unittest.main()
