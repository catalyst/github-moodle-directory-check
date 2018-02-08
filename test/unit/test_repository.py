import inspect
import unittest
from unittest.mock import patch

from app.checker import *


class RepositoryTest(unittest.TestCase):

    def test_it_detects_correct_repository_names(self):
        self.assertFalse(Repository('').has_moodle_repository_name())
        self.assertFalse(Repository('moodle-').has_moodle_repository_name())
        self.assertTrue(Repository('moodle-something').has_moodle_repository_name())

    def test_it_fetches_github_metadata(self):
        versionphps = [
            '$plugin->version="2018020814.43";$plugin->component="local_ninjaturtle";',
            inspect.cleandoc("""
                $plugin->version = '2018020814.43'; // this is the version
                $plugin->component = 'local_ninjaturtle'; // TMNT
            """),
            inspect.cleandoc("""
                $plugin->version = 2018020814.43; // this is the version
                $plugin->component = 'local_ninjaturtle'; // TMNT
            """),
            inspect.cleandoc("""
                $plugin->version        =        2018020814.43;
                $plugin->component\t=\t\t'local_ninjaturtle';
            """),
        ]
        for versionphp in versionphps:
            repository = Repository('moodle-local_ninja')
            with patch.object(GithubConnector, 'get_file', return_value=versionphp):
                repository.fetch_github_metadata(GithubConnector('thetoken'), 'the_user')
            self.assertEquals(2018020814.43, repository.github_version)
            self.assertEquals('local_ninjaturtle', repository.plugin)
