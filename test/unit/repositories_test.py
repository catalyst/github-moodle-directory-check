import unittest
from unittest.mock import patch

from app.checker import *
from test.unit.mock_requests import MockRequests


class RepositoriesTest(unittest.TestCase):

    @patch.object(GithubConnector, 'fetch_repositories', return_value=iter([]))
    def test_it_fetches(self, mock_fetch_repositories):
        github = GithubConnector('thetoken', 'theowner')
        repositories = Repositories(github, 'The Owner')
        repositories.fetch()
        mock_fetch_repositories.assert_called_with()

    def test_it_marks_as_skipped(self):
        repository = Repository('not-a-moodle-thing')
        repositories = Repositories(None, 'Me')
        repositories.categorise_repositories([repository])
        self.assertEqual([repository], repositories.skipped)
        self.assertEqual([], repositories.invalid)
        self.assertEqual([], repositories.unpublished)
        self.assertEqual([], repositories.thirdparty)
        self.assertEqual([], repositories.outdated)
        self.assertEqual([], repositories.uptodate)

    def test_it_marks_as_invalid(self):
        repository = Repository('moodle-not-a-plugin')
        repositories = Repositories(GithubConnector('token', 'theowner'), 'The Maintainer')
        with patch.object(requests, 'get', side_effect=MockRequests.get):
            repositories.categorise_repositories([repository])
        self.assertEqual([], repositories.skipped)
        self.assertEqual([repository], repositories.invalid)
        self.assertEqual([], repositories.unpublished)
        self.assertEqual([], repositories.thirdparty)
        self.assertEqual([], repositories.outdated)
        self.assertEqual([], repositories.uptodate)
