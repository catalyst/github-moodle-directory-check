import unittest
from unittest.mock import patch

from app.checker import *


class RepositoriesTest(unittest.TestCase):

    @patch.object(GithubConnector, 'user_repositories', return_value=iter([]))
    def test_it_fetches(self, mock_user_repositories):
        repositories = Repositories()
        repositories.fetch(GithubConnector('thetoken'), 'theuser')
        mock_user_repositories.assert_called_with('theuser')
