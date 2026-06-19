import unittest
from webapp.app import is_remote


class TestIsRemote(unittest.TestCase):
    def test_is_remote(self):
        self.assertTrue(is_remote({"location": None}))
        self.assertTrue(is_remote({"location": {"name": None}}))
        self.assertTrue(is_remote({"location": {"name": "Home Based - EMEA"}}))
        self.assertFalse(is_remote({"location": {"name": "Paris, France"}}))
