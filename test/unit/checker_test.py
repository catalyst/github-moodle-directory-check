import contextlib
import unittest
from io import StringIO
from unittest.mock import patch

from app.checker import *
from test.unit.mock_integration import *


class CheckerTest(unittest.TestCase):
    @staticmethod
    def mock_fetch_repositories():
        repositories = [
            Repository('my-repository'),
            Repository('moodle-not-a-plugin'),
            Repository('moodle-new-plugin'),
            Repository('moodle-not-mine'),
            Repository('moodle-local_updateme'),
            Repository('moodle-local_published'),
        ]
        return iter(repositories)

    @staticmethod
    @patch.object(requests, 'get', side_effect=MockRequests.get)
    def run_checker(mock_get, args=None):
        if args is None:
            args = ['--token', 'thetoken', '--owner', 'theowner', '--maintainer', 'Catalyst IT']
        stdout = StringIO()
        stderr = StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with patch.object(GithubConnector, 'fetch_repositories', side_effect=CheckerTest.mock_fetch_repositories):
                Checker().run(args)
        return stdout.getvalue(), stderr.getvalue()

    def test_it_lists_all_repository_statuses_in_the_moodle_plugin_directory(self):
        stdout, stderr = self.run_checker()
        self.assertEquals(6, stdout.count('\n'), 'Invalid number of lines printed.')
        self.assertIn('skipped: my-repository', stdout)
        self.assertIn('invalid: moodle-not-a-plugin', stdout)
        self.assertIn('unpublished: moodle-new-plugin', stdout)
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
