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

    def test_it_returns_null_if_cannot_fetch_a_file_from_github(self):
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'), 'some-invalid-username')
        got = github.get_file('some-invalid-repository', 'some-invalid-file')
        self.assertIsNone(got)
