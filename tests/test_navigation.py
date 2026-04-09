import unittest
from unittest.mock import patch
from markupsafe import Markup

import webapp.navigation as navigation


class TestGetCurrentPageBubble(unittest.TestCase):
    def test_returns_matching_bubble_and_sets_active_child(self):
        mock_data = {
            "ai": {
                "path": "/solutions/ai",
                "children": [
                    {"path": "/solutions/ai", "title": "AI overview"},
                ],
            }
        }

        with patch.object(navigation, "secondary_navigation_data", mock_data):
            result = navigation.get_current_page_bubble("/solutions/ai")

        bubble = result["page_bubble"]
        self.assertEqual(bubble["path"], "/solutions/ai")
        self.assertTrue(bubble["children"][0]["active"])

    def test_returns_parent_data_when_child_matches(self):
        mock_data = {
            "data": {
                "path": "/data",
                "children": [
                    {"path": "/data/streaming", "title": "Streaming"},
                ],
                "parent": [{"title": "Solutions"}, {"path": "/solutions"}],
            }
        }

        with patch.object(navigation, "secondary_navigation_data", mock_data):
            result = navigation.get_current_page_bubble("/data/streaming")

        bubble = result["page_bubble"]
        self.assertEqual(bubble["path"], "/data")
        self.assertTrue(
            any(child.get("active") for child in bubble["children"])
        )
        self.assertEqual(bubble["parent_title"], "Solutions")
        self.assertEqual(bubble["parent_path"], "/solutions")

    def test_returns_empty_when_no_match(self):
        with patch.object(navigation, "secondary_navigation_data", {}):
            result = navigation.get_current_page_bubble("/unknown")
        self.assertEqual(result, {"page_bubble": {}})


class TestBuildNavigation(unittest.TestCase):
    def test_renders_meganav_section(self):
        mock_meganav = {"products": {"items": ["item-1"]}}

        with patch.object(navigation, "meganav_data", mock_meganav), patch(
            "webapp.navigation.render_template_string",
            return_value="<div>nav</div>",
        ) as mock_render:
            result = navigation.build_navigation("products", "Products")

        mock_render.assert_called_once_with(
            '{% include "navigation/dropdown.html" %}',
            id="products",
            title="Products",
            section={"items": ["item-1"]},
        )
        self.assertIsInstance(result, Markup)
        self.assertEqual(str(result), "<div>nav</div>")


class TestSplitList(unittest.TestCase):
    def test_splits_evenly(self):
        self.assertEqual(
            navigation.split_list([1, 2, 3, 4], 2),
            [[1, 2], [3, 4]],
        )

    def test_splits_with_remainder(self):
        self.assertEqual(
            navigation.split_list([1, 2, 3, 4, 5], 3),
            [[1, 2], [3, 4], [5]],
        )

    def test_raises_on_invalid_parts(self):
        with self.assertRaises(ValueError):
            navigation.split_list([1, 2], 0)


if __name__ == "__main__":
    unittest.main()
