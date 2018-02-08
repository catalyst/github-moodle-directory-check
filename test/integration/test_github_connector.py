import os
import unittest

from app.checker import *


class GithubConnectorTest(unittest.TestCase):

    def test_it_gets_user_repositories(self):
        should_find = 'github-moodle-directory-check'
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'))
        for repository in github.user_repositories('catalyst'):
            if repository.name == should_find:
                return
        self.fail('Repository not found: ' + should_find)

    def test_it_fetches_a_file_from_github(self):
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'))
        readme = github.get_file('catalyst', 'github-moodle-directory-check', 'README.md')
        self.assertIn('# GitHub & Moodle Plugin Directory', readme)
