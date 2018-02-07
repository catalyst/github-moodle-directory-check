#!/usr/bin/env python3

from argparse import ArgumentParser

import sys
from github import Github


class CheckerArgumentParser(ArgumentParser):
    def __init__(self, args):
        super().__init__()
        self.add_help = True
        self.add_argument('--token', help='GitHub Token', required=True)
        self.add_argument('--user', help='GitHub User', required=True)
        args = self.parse_args(args)
        self.token = args.token
        self.user = args.user


class Repositories:
    def __init__(self):
        self.skipped = ['my-repository']
        self.invalid = ['moodle-not-a-plugin']
        self.outdated = ['moodle-local_updateme']
        self.updated = ['moodle-local_published']


class GithubConnector:
    def __init__(self, token):
        self.github = Github(token)

    def user_repositories(self, username):
        for repository in self.github.get_user(username).get_repos():
            yield str(repository.name)


class Checker:
    @staticmethod
    def run(argv):
        arguments = CheckerArgumentParser(argv)
        repositories = Repositories()
        for group in ['skipped', 'invalid', 'outdated', 'updated']:
            for repository in getattr(repositories, group):
                print('{:>8}: {}'.format(group, repository))


if __name__ == "__main__":
    Checker().run(sys.argv[1:])
