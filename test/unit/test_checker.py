import contextlib
import unittest
from io import StringIO
from unittest.mock import patch

from app.checker import *


class CheckerTest(unittest.TestCase):
    @staticmethod
    def mock_get_file(repository, file):
        if file != 'version.php':
            return None
        if repository == 'moodle-not-mine':
            return '$plugin->version="2018020915";$plugin->component="local_notmyplugin";'
        if repository == 'moodle-local_updateme':
            return '$plugin->version="2018020814.43";$plugin->component="local_ninjaturtle";'
        if repository == 'moodle-local_published':
            return '$plugin->version="2018020913.29";$plugin->component="local_ninjaturtle";'
        return None

    @staticmethod
    def run_checker(args=None):
        if args is None:
            args = ['--token', 'thetoken', '--owner', 'theowner']
        stdout = StringIO()
        stderr = StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            repositories = [
                Repository('my-repository'),
                Repository('moodle-not-a-plugin'),
                Repository('moodle-not-mine'),
                Repository('moodle-local_updateme'),
                Repository('moodle-local_published'),
            ]
            with patch.object(GithubConnector, 'fetch_repositories', return_value=iter(repositories)):
                with patch.object(GithubConnector, 'get_file', side_effect=CheckerTest.mock_get_file):
                    Checker().run(args)
        return stdout.getvalue(), stderr.getvalue()

    def test_it_lists_all_repository_statuses_in_the_moodle_plugin_directory(self):
        stdout, stderr = self.run_checker()
        self.assertEquals(5, stdout.count('\n'), 'Invalid number of lines printed.')
        self.assertIn('skipped: my-repository', stdout)
        self.assertIn('invalid: moodle-not-a-plugin', stdout)
        self.assertIn('thirdparty: moodle-not-mine', stdout)
        self.assertIn('outdated: moodle-local_updateme', stdout)
        self.assertIn('uptodate: moodle-local_published', stdout)

    def test_it_aligns_the_group_name(self):
        stdout, stderr = self.run_checker()
        lines = stdout.strip('\n').split('\n')
        position = None
        for line in lines:
            found = line.find(':')
            if position is None:
                position = found
            else:
                self.assertEquals(position, found)

    def test_it_shows_help_if_missing_parameters(self):
        with self.assertRaises(SystemExit):
            stdout, stderr = self.run_checker([])
            self.assertIn('arguments are required', stderr)
