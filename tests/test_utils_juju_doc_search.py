import unittest
from unittest.mock import MagicMock, patch

from webapp.utils import juju_doc_search


class TestExtractFullDomain(unittest.TestCase):
    def test_canonical_docs_domain(self):
        result = {"domain": "https://documentation.ubuntu.com", "path": "/juju/some-page"}
        self.assertEqual(
            juju_doc_search.extract_full_domain(result), "documentation.ubuntu.com/juju"
        )

    def test_ops_docs_domain(self):
        result = {"domain": "https://ops.readthedocs.io", "path": "/en/latest/"}
        self.assertEqual(juju_doc_search.extract_full_domain(result), "ops.readthedocs.io")


class TestFetchSearchResults(unittest.TestCase):
    @patch("webapp.utils.juju_doc_search.requests.get")
    def test_fetch_results_multiple_projects(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"results": [{"title": "match"}]}),
        )

        results = juju_doc_search.fetch_search_results(
            juju_doc_search.RTD_HOSTED_API, "juju", ["proj-a", "proj-b"]
        )

        self.assertEqual(results, [{"title": "match"}])
        mock_get.assert_called_once()
        called_params = mock_get.call_args.kwargs["params"]["q"]
        self.assertIn("project:proj-a", called_params)
        self.assertIn("project:proj-b", called_params)

    @patch("webapp.utils.juju_doc_search.requests.get")
    def test_fetch_results_handles_errors(self, mock_get):
        mock_get.side_effect = juju_doc_search.requests.exceptions.Timeout()
        self.assertEqual(
            juju_doc_search.fetch_search_results("https://example.com", "juju"), []
        )


class TestSearchAllDocs(unittest.TestCase):
    @patch("webapp.utils.juju_doc_search.fetch_search_results")
    def test_search_all_docs_combines_results(self, mock_fetch):
        def _fake_fetch(api_url, query, projects=None):
            if api_url == juju_doc_search.RTD_HOSTED_API:
                return [{"title": "hosted"}]
            return [{"title": "ops"}]

        mock_fetch.side_effect = _fake_fetch

        results = juju_doc_search.search_all_docs("juju")

        self.assertEqual(len(results), 2)
        self.assertCountEqual(
            [item["title"] for item in results],
            ["hosted", "ops"],
        )


class TestCalculateRelevance(unittest.TestCase):
    def test_calculate_relevance_boosts_how_to(self):
        result = {
            "title": "How to deploy juju",
            "blocks": [{"content": "Learn how to deploy."}],
            "domain": "https://documentation.ubuntu.com",
            "path": "/juju/deploy/",
        }
        self.assertGreater(
            juju_doc_search.calculate_relevance(result, "deploy"),
            0,
        )


class TestProcessAndSortResults(unittest.TestCase):
    @patch("webapp.utils.juju_doc_search.calculate_relevance", side_effect=[0.5, 0.9])
    def test_process_and_sort_results(self, mock_relevance):
        raw_results = [
            {
                "title": "First",
                "blocks": [{"content": "First content"}],
                "domain": "https://documentation.ubuntu.com",
                "path": "/juju/first",
            },
            {
                "title": "Second",
                "blocks": [{"content": "Second content is longer" * 20}],
                "domain": "https://documentation.ubuntu.com",
                "path": "/juju/second",
            },
        ]

        processed = juju_doc_search.process_and_sort_results(
            raw_results, "juju", max_length=50
        )

        self.assertEqual(processed[0]["title"], "Second")
        self.assertTrue(processed[0]["short_content"].endswith("..."))
        self.assertIn("search_url", processed[0])


if __name__ == "__main__":
    unittest.main()