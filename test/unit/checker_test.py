import contextlib
import unittest
from io import StringIO
from unittest.mock import patch
from urllib import parse

from app.checker import *


class CheckerTestMockResponse:
    def __init__(self, plugin):
        (maintainer) = CheckerTest.mock_requests_get_plugin_data(plugin)
        if maintainer is None:
            self.status_code = 404
            self.text = 'Not found.'
        else:
            maintainer = '<div class="maintainedby"><span class="name">{}</span></div>'.format(maintainer)
            self.status_code = 200
            self.text = '<html>{}</html>'.format(maintainer)


class CheckerTest(unittest.TestCase):
    @staticmethod
    def mock_requests_get(url):
        query = parse.urlparse(url).query
        plugin = parse.parse_qs(query)['plugin'][0]
        return CheckerTestMockResponse(plugin)

    @staticmethod
    def mock_requests_get_plugin_data(plugin):
        if plugin == 'local_newplugin':
            return None
        if plugin == 'local_notmyplugin':
            return 'Someone Else'
        if plugin == 'local_ninjaturtle':
            return 'Catalyst IT'
        raise Exception('Invalid mock_requests_get_plugin_data for: ' + plugin)

    @staticmethod
    def mock_get_file(repository, file):
        if file != 'version.php':
            return None
        if repository == 'moodle-new-plugin':
            return '$plugin->version="2018021211.58";$plugin->component="local_newplugin";'
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
            args = ['--token', 'thetoken', '--owner', 'theowner', '--maintainer', 'Catalyst IT']
        stdout = StringIO()
        stderr = StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            repositories = [
                Repository('my-repository'),
                Repository('moodle-not-a-plugin'),
                Repository('moodle-new-plugin'),
                Repository('moodle-not-mine'),
                Repository('moodle-local_updateme'),
                Repository('moodle-local_published'),
            ]
            with patch.object(GithubConnector, 'fetch_repositories', return_value=iter(repositories)):
                with patch.object(GithubConnector, 'get_file', side_effect=CheckerTest.mock_get_file):
                    with patch.object(requests, 'get', side_effect=CheckerTest.mock_requests_get):
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
