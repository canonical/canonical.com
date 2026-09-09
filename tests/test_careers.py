import logging
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from webapp.careers import (
    DEPARTMENT_LIST,
    get_all_departments,
    group_by_department,
)


logging.getLogger("talisker.context").disabled = True


def _make_vacancy(*department_slugs):
    """
    Build a minimal vacancy-like object.

    ``group_by_department`` only relies on each vacancy exposing a
    ``departments`` list whose items have a ``slug`` attribute, so we
    avoid constructing full ``Vacancy`` instances here.
    """
    departments = [SimpleNamespace(slug=slug) for slug in department_slugs]
    return SimpleNamespace(departments=departments)


class TestGroupByDepartment(unittest.TestCase):
    def test_includes_every_known_department(self):
        """
        Every department in DEPARTMENT_LIST should be present as a key,
        even when there are no vacancies at all.
        """
        grouped = group_by_department([])

        self.assertEqual(list(grouped.keys()), list(DEPARTMENT_LIST.keys()))

    def test_order_matches_department_list(self):
        """
        The order of the returned dict should always match the order of
        DEPARTMENT_LIST, regardless of the vacancy data.
        """
        vacancies = [
            _make_vacancy("legal"),
            _make_vacancy("engineering"),
            _make_vacancy("sales"),
        ]

        grouped = group_by_department(vacancies)

        self.assertEqual(list(grouped.keys()), list(DEPARTMENT_LIST.keys()))

    def test_preserves_department_metadata(self):
        """
        Each grouped department should keep its original metadata and gain
        an empty "vacancies" list when no vacancies match.
        """
        grouped = group_by_department([])

        engineering = grouped["engineering"]
        self.assertEqual(engineering["name"], "Engineering")
        self.assertEqual(engineering["slug"], "engineering")
        self.assertEqual(
            engineering["icon"], DEPARTMENT_LIST["engineering"]["icon"]
        )
        self.assertEqual(engineering["vacancies"], [])

    def test_assigns_vacancies_to_their_department(self):
        """
        Vacancies should be appended to the department that matches their
        department slug.
        """
        engineering_vacancy = _make_vacancy("engineering")
        sales_vacancy = _make_vacancy("sales")

        grouped = group_by_department([engineering_vacancy, sales_vacancy])

        self.assertEqual(
            grouped["engineering"]["vacancies"], [engineering_vacancy]
        )
        self.assertEqual(grouped["sales"]["vacancies"], [sales_vacancy])
        self.assertEqual(grouped["legal"]["vacancies"], [])

    def test_vacancy_in_multiple_departments(self):
        """
        A vacancy that belongs to several departments should appear under
        each matching department.
        """
        vacancy = _make_vacancy("engineering", "product")

        grouped = group_by_department([vacancy])

        self.assertIn(vacancy, grouped["engineering"]["vacancies"])
        self.assertIn(vacancy, grouped["product"]["vacancies"])

    def test_ignores_unknown_department_slugs(self):
        """
        Vacancies belonging to an unknown department should be dropped and
        must not create new keys.
        """
        vacancy = _make_vacancy("nonexistent-department")

        grouped = group_by_department([vacancy])

        self.assertNotIn("nonexistent-department", grouped)
        self.assertEqual(list(grouped.keys()), list(DEPARTMENT_LIST.keys()))
        for department in grouped.values():
            self.assertEqual(department["vacancies"], [])


class TestGetAllDepartments(unittest.TestCase):
    def _make_greenhouse(self, vacancies):
        greenhouse = MagicMock()
        greenhouse.get_vacancies.return_value = vacancies
        return greenhouse

    def test_returns_grouped_departments_and_overview(self):
        """
        get_all_departments should return a (grouped, overview) tuple where
        the overview summarises each department.
        """
        greenhouse = self._make_greenhouse(
            [_make_vacancy("engineering"), _make_vacancy("engineering")]
        )

        all_departments, overview = get_all_departments(greenhouse)

        self.assertEqual(
            list(all_departments.keys()), list(DEPARTMENT_LIST.keys())
        )
        self.assertEqual(len(overview), len(DEPARTMENT_LIST))

    def test_overview_entry_shape_and_counts(self):
        """
        Each overview entry should expose name, count, slug and icon, and
        the count should reflect the number of matching vacancies.
        """
        greenhouse = self._make_greenhouse(
            [
                _make_vacancy("engineering"),
                _make_vacancy("engineering"),
                _make_vacancy("sales"),
            ]
        )

        _, overview = get_all_departments(greenhouse)
        overview_by_slug = {entry["slug"]: entry for entry in overview}

        self.assertEqual(
            set(overview_by_slug["engineering"].keys()),
            {"name", "count", "slug", "icon"},
        )
        self.assertEqual(overview_by_slug["engineering"]["count"], 2)
        self.assertEqual(overview_by_slug["sales"]["count"], 1)
        self.assertEqual(overview_by_slug["legal"]["count"], 0)
        self.assertEqual(
            overview_by_slug["engineering"]["name"], "Engineering"
        )
        self.assertEqual(
            overview_by_slug["engineering"]["icon"],
            DEPARTMENT_LIST["engineering"]["icon"],
        )

    def test_overview_order_matches_department_list(self):
        """
        The overview order should follow DEPARTMENT_LIST.
        """
        greenhouse = self._make_greenhouse([])

        _, overview = get_all_departments(greenhouse)

        self.assertEqual(
            [entry["slug"] for entry in overview],
            list(DEPARTMENT_LIST.keys()),
        )


if __name__ == "__main__":
    unittest.main()
