import contextlib
import shlex
from io import StringIO
from unittest.mock import patch

import requests
from behave import *

from app.checker import *
from app.repository import Repository
from test.unit.mock_requests import *


class IntegrationTest:
    @staticmethod
    def run_checker(args, mocked_repositories):
        stdout = StringIO()
        stderr = StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with patch.object(GithubConnector, 'fetch_repositories', side_effect=[mocked_repositories]):
                with patch.object(requests, 'get', side_effect=MockRequests.get):
                    try:
                        Checker().run(args)
                    except SystemExit:
                        pass
        return stdout.getvalue(), stderr.getvalue()

    @staticmethod
    @given(u'the user "theowner" on GitHub has the following repositories')
    def step_impl(context):
        context.repositories = []
        for row in context.table.rows:
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
    @then(u'the output should be')
    def step_impl(context):
        expected = str(context.text) + '\n'
        if context.stdout != expected:
            raise AssertionError('Expected:\n{}\nFound:\n{}\n'.format(expected, context.stdout))

    @staticmethod
    @then(u'the error output should be')
    def step_impl(context):
        expected = str(context.text) + '\n'
        if context.stderr != expected:
            raise AssertionError('Expected:\n{}\nFound:\n{}\n'.format(expected, context.stderr))

    @staticmethod
    @then(u'the error output should contain "{text}"')
    def step_impl(context, text):
        if text not in context.stderr:
            raise AssertionError('Not found:\n{}\nin:\n{}\n'.format(text, context.stderr))

    @staticmethod
    @then(u'the output should be empty')
    def step_impl(context):
        if context.stdout != '':
            raise NotImplementedError(u'stdout not empty: {}' + format(context.stdout))

    @staticmethod
    @then(u'the error output should be empty')
    def step_impl(context):
        if context.stderr != '':
            raise NotImplementedError(u'stderr not empty: {}' + format(context.stderr))
