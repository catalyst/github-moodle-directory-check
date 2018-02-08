import os
import unittest

from app.checker import *


class GithubConnectorTest(unittest.TestCase):

    def test_it_gets_user_repositories(self):
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'))
        repositories = list(github.user_repositories('catalyst'))
        self.assertIn('github-moodle-directory-check', repositories)

    def test_it_fetches_a_file_from_github(self):
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'))
        readme = github.get_file('catalyst', 'github-moodle-directory-check', 'README.md')
        self.assertIn('# GitHub & Moodle Plugin Directory', readme)
