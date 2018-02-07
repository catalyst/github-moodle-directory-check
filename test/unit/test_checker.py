import contextlib
import unittest
from io import StringIO

from app.checker import *


class CheckerTest(unittest.TestCase):

    def test_it_lists_all_repository_statuses_in_the_moodle_plugin_directory(self):
        stdout = StringIO()
        with contextlib.redirect_stdout(stdout):
            Checker().run()
        output = stdout.getvalue()
        self.assertEquals(4, output.count('\n'), 'Invalid number of lines printed.')
        self.assertIn('skipped: my-repository', output)
        self.assertIn('invalid: moodle-not-a-plugin', output)
        self.assertIn('outdated: moodle-local_updateme', output)
        self.assertIn('updated: moodle-local_published', output)


