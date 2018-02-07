import os
import unittest

from app.checker import *


class GithubConnectorTest(unittest.TestCase):

    def test_it_gets_user_repositories(self):
        github = GithubConnector(os.environ.get('TEST_GITHUB_TOKEN'))
        repositories = list(github.user_repositories('catalyst'))
        self.assertIn('github-moodle-directory-check', repositories)
