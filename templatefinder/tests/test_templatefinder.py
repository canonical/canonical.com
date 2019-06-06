import unittest

from unittest.mock import patch
from .. import TemplateFinder


class TestTemplateFinder(unittest.TestCase):
    def test_dispatch_request(self):
        templatefinder = TemplateFinder()
        result = templatefinder.dispatch_request()
