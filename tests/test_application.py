import unittest

from webapp.application import _milestones_progress

all_stages = [
    {"name": "Application Review"},
    {"name": "Written Interview"},
    {"name": "Devskiller"},
    {"name": "Thomas International - GIA"},
    {"name": "Hold"},
    {"name": "Technical Exercise"},
    {"name": "Early Stage Interviews"},
    {"name": "Thomas International - PPA"},
    {"name": "Talent Interview"},
    {"name": "Late Stage Interviews"},
    {"name": "Shortlist"},
    {"name": "Executive Review"},
    {"name": "Offer"},
]


class TestApplicationPageHelpers(unittest.TestCase):
    def test_milestone_progress_current_stage_defined(self):
        self.assertDictEqual(
            _milestones_progress({"name": "Devskiller"}, all_stages),
            {
                "application": True,
                "assessment": True,
                "early_stage": True,
                "late_stage": False,
                "offer": False,
            },
        )

    def test_milestone_progress_current_stage_undefined(self):
        self.assertDictEqual(
            _milestones_progress(None, all_stages),
            {
                "application": False,
                "assessment": False,
                "early_stage": False,
                "late_stage": False,
                "offer": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
