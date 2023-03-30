import unittest

from webapp.application import (
    _milestones_progress,
    _sort_stages_by_milestone,
    _get_gia_feedback,
)

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
    def test_sort_stages_by_milestone_sort_and_filter(self):
        milestones = {"m1": ["s1", "s2"], "m2": ["s3"]}
        stages_to_sort = ["s3", "s1", "s4", "s2", "s5"]
        self.assertListEqual(
            _sort_stages_by_milestone(stages_to_sort, milestones),
            ["s1", "s2", "s3"],
        )

    def test_sort_stages_by_milestone_empty_stages(self):
        milestones = {"m1": ["s1", "s2"], "m2": ["s3"]}
        stages_to_sort = []
        self.assertListEqual(
            _sort_stages_by_milestone(stages_to_sort, milestones),
            [],
        )

    def test_sort_stages_by_milestone_empty_milestones(self):
        milestones = {}
        stages_to_sort = ["s1", "s2"]
        self.assertListEqual(
            _sort_stages_by_milestone(stages_to_sort, milestones),
            [],
        )

    def test_milestone_progress_current_stage_defined(self):
        self.assertDictEqual(
            _milestones_progress(
                all_stages, {"name": "Early Stage Interviews"}
            ),
            {
                "application": True,
                "assessment": True,
                "early_stage": True,
                "late_stage": False,
                "offer": False,
            },
        )

    def test_milestone_progress_unordered_stages_list(self):
        all_stages = [
            {"name": "Offer"},
            {"name": "Application Review"},
            {"name": "Written Interview"},
            {"name": "Devskiller"},
            {"name": "Thomas International - GIA"},
            {"name": "Hold"},
            {"name": "Late Stage Interviews"},
            {"name": "Talent Interview"},
            {"name": "Technical Exercise"},
            {"name": "Early Stage Interviews"},
            {"name": "Shortlist"},
            {"name": "Thomas International - PPA"},
            {"name": "Executive Review"},
        ]
        self.assertDictEqual(
            _milestones_progress(all_stages, {"name": "Offer"}),
            {
                "application": True,
                "assessment": True,
                "early_stage": True,
                "late_stage": True,
                "offer": True,
            },
        )

    def test_milestone_progress_current_stage_undefined(self):
        self.assertDictEqual(
            _milestones_progress(all_stages, None),
            {
                "application": False,
                "assessment": False,
                "early_stage": False,
                "late_stage": False,
                "offer": False,
            },
        )


class TestGetGiaFeedback(unittest.TestCase):
    def test_gia_feedback_is_found_correctly(self):
        attachments = [
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:23.973Z",
            },
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:11.164Z",
            },
        ]
        self.assertDictEqual(
            _get_gia_feedback(attachments),
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
        )

    def test_gia_feedback_returns_one_if_more_available(self):
        attachments = [
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:23.973Z",
            },
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:11.164Z",
            },
        ]
        self.assertDictEqual(
            _get_gia_feedback(attachments),
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
        )

    def test_gia_feedback_not_found(self):
        attachments = [
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:23.973Z",
            },
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:11.164Z",
            },
        ]
        self.assertEqual(_get_gia_feedback(attachments), None)

    def test_gia_feedback_not_found_when_empty(self):
        attachments = []
        self.assertEqual(_get_gia_feedback(attachments), None)


if __name__ == "__main__":
    unittest.main()
