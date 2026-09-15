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

    def test_match_scopes_bubble_to_its_own_prefixes(self):
        # "kafka" and "opensearch" both link to /data but are scoped with
        # "match" so each only applies to its own pages
        mock_data = {
            "data": {
                "path": "/data",
                "children": [
                    {"path": "/data/services", "title": "Services"},
                ],
            },
            "kafka": {
                "path": "/data",
                "match": "/data/kafka",
                "children": [
                    {"path": "/data/services", "title": "Services"},
                    {"path": "/data/kafka/docs", "title": "Docs"},
                ],
            },
            "opensearch": {
                "path": "/data",
                "match": "/data/opensearch",
                "children": [
                    {"path": "/data/services", "title": "Services"},
                    {"path": "/data/opensearch/docs", "title": "Docs"},
                ],
            },
        }

        with patch.object(navigation, "secondary_navigation_data", mock_data):
            kafka = navigation.get_current_page_bubble("/data/kafka")
            kafka_child = navigation.get_current_page_bubble(
                "/data/kafka/managed"
            )
            opensearch = navigation.get_current_page_bubble("/data/opensearch")
            opensearch_docs = navigation.get_current_page_bubble(
                "/data/opensearch/docs"
            )
            services = navigation.get_current_page_bubble("/data/services")

        def docs_path(result):
            return result["page_bubble"]["children"][1]["path"]

        self.assertEqual(docs_path(kafka), "/data/kafka/docs")
        self.assertEqual(docs_path(kafka_child), "/data/kafka/docs")
        self.assertEqual(docs_path(opensearch), "/data/opensearch/docs")
        self.assertEqual(docs_path(opensearch_docs), "/data/opensearch/docs")
        self.assertTrue(
            opensearch_docs["page_bubble"]["children"][1]["active"]
        )
        # Scoped bubbles are skipped for exact child matches outside their
        # scope, so a shared child like /data/services falls back to the
        # unscoped bubble
        self.assertNotIn("match", services["page_bubble"])
        self.assertEqual(len(services["page_bubble"]["children"]), 1)
        self.assertTrue(services["page_bubble"]["children"][0]["active"])

    def test_match_accepts_a_list_of_prefixes(self):
        mock_data = {
            "scoped": {
                "path": "/data",
                "match": ["/data/one", "/data/two"],
                "children": [],
            },
        }

        with patch.object(navigation, "secondary_navigation_data", mock_data):
            one = navigation.get_current_page_bubble("/data/one/page")
            two = navigation.get_current_page_bubble("/data/two")
            other = navigation.get_current_page_bubble("/data/three")

        self.assertEqual(one["page_bubble"]["path"], "/data")
        self.assertEqual(two["page_bubble"]["path"], "/data")
        self.assertEqual(other, {"page_bubble": {}})


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
