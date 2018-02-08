import contextlib
import unittest
from io import StringIO
from unittest.mock import patch

from app.checker import *


class CheckerTest(unittest.TestCase):
    @staticmethod
    def run_checker(args=None):
        if args is None:
            args = ['--token', 'thetoken', '--user', 'theuser']
        stdout = StringIO()
        stderr = StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            repositories = [
                Repository('my-repository'),
                Repository('moodle-not-a-plugin'),
                Repository('moodle-local_updateme'),
                Repository('moodle-local_published'),
            ]
            with patch.object(GithubConnector, 'user_repositories', return_value=iter(repositories)):
                Checker().run(args)
        return stdout.getvalue(), stderr.getvalue()

    def test_it_lists_all_repository_statuses_in_the_moodle_plugin_directory(self):
        stdout, stderr = self.run_checker()
        self.assertEquals(4, stdout.count('\n'), 'Invalid number of lines printed.')
        self.assertIn('skipped: my-repository', stdout)
        self.assertIn('invalid: moodle-not-a-plugin', stdout)
        self.assertIn('outdated: moodle-local_updateme', stdout)
        self.assertIn('updated: moodle-local_published', stdout)

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
