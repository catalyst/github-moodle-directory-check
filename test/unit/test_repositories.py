import unittest
from unittest.mock import patch

from app.checker import *


class RepositoriesTest(unittest.TestCase):

    @patch.object(GithubConnector, 'user_repositories', return_value=iter([]))
    def test_it_fetches(self, mock_user_repositories):
        github = GithubConnector('thetoken', 'theuser')
        repositories = Repositories(github)
        repositories.fetch()
        mock_user_repositories.assert_called_with()

    def test_it_marks_as_skipped(self):
        repository = Repository('not-a-moodle-thing')
        repositories = Repositories(None)
        repositories.categorise_repositories([repository])
        self.assertEqual([repository], repositories.skipped)
        self.assertEqual([], repositories.invalid)
        self.assertEqual([], repositories.outdated)
        self.assertEqual([], repositories.updated)

    def test_it_marks_as_invalid(self):
        repository = Repository('moodle-local_ninja')
        repositories = Repositories(GithubConnector('token', 'user'))
        with patch.object(GithubConnector, 'get_file', return_value=None):
            repositories.categorise_repositories([repository])
        self.assertEqual([], repositories.skipped)
        self.assertEqual([repository], repositories.invalid)
        self.assertEqual([], repositories.outdated)
        self.assertEqual([], repositories.updated)
