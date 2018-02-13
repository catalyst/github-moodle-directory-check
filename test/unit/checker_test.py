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
    def run_checker(extra_args=None, args=None):
        if args is None:
            args = ['--token', 'thetoken', '--owner', 'theowner', '--maintainer', 'Catalyst IT']
        if extra_args is not None:
            args += extra_args
        stdout = StringIO()
        stderr = StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with patch.object(GithubConnector, 'fetch_repositories', side_effect=CheckerTest.mock_fetch_repositories):
                with patch.object(requests, 'get', side_effect=MockRequests.get):
                    Checker().run(args)
        return stdout.getvalue(), stderr.getvalue()

    def test_it_lists_all_repository_statuses_in_the_moodle_plugin_directory(self):
        stdout, stderr = self.run_checker(['-q'])
        self.assertEquals(6, stdout.count('\n'), 'Invalid number of lines printed:\n' + stdout)
        self.assertIn('skipped: my-repository', stdout)
        self.assertIn('invalid: moodle-not-a-plugin', stdout)
        self.assertIn('unpublished: moodle-new-plugin', stdout)
        self.assertIn('thirdparty: moodle-not-mine', stdout)
        self.assertIn('outdated: moodle-local_updateme', stdout)
        self.assertIn('uptodate: moodle-local_published', stdout)

    def test_it_shows_verbose_messages(self):
        stdout, stderr = self.run_checker(['-v'])
        stderr = stderr.strip().split('\n')
        self.assertGreaterEqual(len(stderr), 6)
        stderr = iter(stderr)
        self.assertIn('GitHub for: theowner', next(stderr))
        self.assertIn('Analysing: my-repository', next(stderr))
        self.assertIn('Analysing: moodle-not-a-plugin', next(stderr))
        self.assertIn('Analysing: moodle-new-plugin', next(stderr))
        self.assertIn('Analysing: moodle-not-mine', next(stderr))
        self.assertIn('Analysing: moodle-local_updateme', next(stderr))
        self.assertIn('Analysing: moodle-local_published', next(stderr))

    def test_it_aligns_the_group_name(self):
        stdout, stderr = self.run_checker()
        lines = stdout.strip('\n').split('\n')
        position = None
        for line in lines:
            found = line.find(':')
            if found == -1:
                continue
            if position is None:
                position = found
            else:
                self.assertEquals(position, found)

    def test_it_shows_dots_for_each_repository_processed(self):
        stdout, stderr = self.run_checker()
        stdout = stdout.strip().split('\n')
        self.assertGreaterEqual(len(stdout), 1)
        stdout = stdout[0]
        # One dot for fetching repositories on GitHub plus one for each repository
        expected = '.' * (len(list(CheckerTest.mock_fetch_repositories())) + 1)
        self.assertEquals(stdout, expected)

    def test_it_shows_help_if_missing_parameters(self):
        with self.assertRaises(SystemExit):
            stdout, stderr = self.run_checker([], [])
            self.assertIn('arguments are required', stderr)
