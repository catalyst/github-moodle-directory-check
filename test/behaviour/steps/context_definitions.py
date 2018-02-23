import contextlib
import shlex
from io import StringIO
from unittest.mock import patch

from behave import *

from app.checker import *
from test.unit.mock_requests import *


class IntegrationTest:
    @staticmethod
    def run_checker(args, mocked_repositories):
        stdout = StringIO()
        stderr = StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with patch.object(GithubConnector, 'fetch_repositories', side_effect=[mocked_repositories]):
                with patch.object(requests, 'get', side_effect=MockRequests.get):
                    Checker().run(args)
        return stdout.getvalue(), stderr.getvalue()

    @staticmethod
    @given(u'the user "theowner" on GitHub has the following repositories')
    def step_impl(context):
        context.repositories = []
        for row in context.table:
            context.repositories.append(Repository(row[0]))

    @staticmethod
    @when(u'I run "{command}"')
    def step_impl(context, command):
        arguments = shlex.split(command)
        if arguments[0] != 'checker.py':
            raise ValueError('Command must be checker.py, found: {}'.format(arguments[0]))
        del arguments[0]
        stdout, stderr = IntegrationTest.run_checker(arguments, context.repositories)
        context.stdout = stdout
        context.stderr = stderr

    @staticmethod
    @then(u'the output should have the following plugins')
    def step_impl(context):
        expectedrows = len(context.table.rows)
        stdout = context.stdout
        if expectedrows != stdout.count('\n'):
            raise AssertionError('Invalid number of lines printed: {}'.format(stdout.count('\n')))
        for row in context.table:
            expected = row[0]
            if expected not in stdout:
                raise AssertionError('Cannot find int stdout: {}'.format(expected))

    @staticmethod
    @then(u'the error output should be empty')
    def step_impl(context):
        if context.stderr != '':
            raise NotImplementedError(u'stderr not empty: {}' + format(context.stderr))
