import unittest
from unittest.mock import patch

import requests

from app.moodle_plugin_directory_page import MoodlePluginDirectoryPage
from test.unit.mock_requests import MockRequests


class MoodlePluginDirectoryPageTest(unittest.TestCase):

    def test_it_detects_maintainers(self):
        page = MoodlePluginDirectoryPage('auth_saml2')
        with patch.object(requests, 'get', side_effect=MockRequests.get):
            page.fetch()
        self.assertTrue(page.has_maintainer('Catalyst IT'))
        self.assertTrue(page.has_maintainer('Brendan Heywood'))
        self.assertTrue(page.has_maintainer('Adam Riddell'))
        self.assertTrue(page.has_maintainer('Daniel Thee Roperto'))
        self.assertFalse(page.has_maintainer('John Doe'))

    def test_it_detects_version(self):
        page = MoodlePluginDirectoryPage('auth_saml2')
        with patch.object(requests, 'get', side_effect=MockRequests.get):
            page.fetch()
        self.assertTrue(page.has_version(2018020200))
        self.assertFalse(page.has_version(2018020201))
