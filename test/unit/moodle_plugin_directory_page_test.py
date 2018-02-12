import unittest
from unittest.mock import patch

import os

from app.checker import *


class MoodlePluginDirectoryPageTest(unittest.TestCase):
    @staticmethod
    def mock_fetch_html(url):
        class MockResponse:
            def __init__(self):
                self.status_code = 200
                file = os.path.dirname(__file__)
                file = os.path.join(file, '..', 'fixtures', 'auth_saml2.html')
                with open(file, 'r') as file:
                    self.text = file.read()

        return MockResponse()

    def test_it_detects_maintainers(self):
        page = MoodlePluginDirectoryPage('some-plugin')
        with patch.object(requests, 'get', side_effect=MoodlePluginDirectoryPageTest.mock_fetch_html):
            page.fetch()
        self.assertTrue(page.has_maintainer('Catalyst IT'))
        self.assertTrue(page.has_maintainer('Brendan Heywood'))
        self.assertTrue(page.has_maintainer('Adam Riddell'))
        self.assertTrue(page.has_maintainer('Daniel Thee Roperto'))
        self.assertFalse(page.has_maintainer('John Doe'))

    def test_it_detects_version(self):
        page = MoodlePluginDirectoryPage('some-plugin')
        with patch.object(requests, 'get', side_effect=MoodlePluginDirectoryPageTest.mock_fetch_html):
            page.fetch()
        self.assertTrue(page.has_version(2018020200))
        self.assertFalse(page.has_version(2018020201))
