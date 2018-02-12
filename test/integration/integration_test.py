import os
import unittest

from app.checker import *


class IntegrationTest(unittest.TestCase):

    def test_it_fetches_repositories(self):
        should_find = 'github-moodle-directory-check'
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'), 'catalyst')
        for repository in github.fetch_repositories():
            if repository.name == should_find:
                return
        self.fail('Repository not found: ' + should_find)

    def test_it_fetches_a_file_from_github(self):
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'), 'catalyst')
        readme = github.get_file('github-moodle-directory-check', 'README.md')
        self.assertIn('# GitHub & Moodle Plugin Directory', readme)

    def test_it_returns_none_if_cannot_fetch_a_file_from_github(self):
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'), 'some-invalid-username')
        got = github.get_file('some-invalid-repository', 'some-invalid-file')
        self.assertIsNone(got)

    def test_it_fetches_metadata_from_moodle_plugin_directory(self):
        directory = MoodlePluginDirectoryPage('auth_saml2')
        directory.fetch()
        self.assertIsNotNone(directory.html)
        self.assertTrue(directory.has_maintainer('Catalyst IT'))
        self.assertFalse(directory.has_maintainer('John Doe'))
        self.assertFalse(directory.has_version('1982050318'))

    def test_it_returns_none_if_cannot_fetch_metadata_from_moodle_plugin_directory(self):
        directory = MoodlePluginDirectoryPage('someinvalidplugin')
        directory.text = 'something'
        directory.pyquery = 'something'
        directory.fetch()
        self.assertIsNone(directory.html)
        self.assertIsNone(directory.pyquery)
