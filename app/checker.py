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
        self.skipped = None
        self.invalid = None
        self.outdated = None
        self.updated = None

    def fetch(self, github, user):
        self.skipped = []
        self.invalid = []
        self.outdated = []
        self.updated = []
        repositories = github.user_repositories(user)
        self.skipped.append(next(repositories))
        self.invalid.append(next(repositories))
        self.outdated.append(next(repositories))
        self.updated.append(next(repositories))


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
        github = GithubConnector(arguments.token)
        repositories.fetch(github, arguments.user)
        for group in ['skipped', 'invalid', 'outdated', 'updated']:
            for repository in getattr(repositories, group):
                print('{:>8}: {}'.format(group, repository))


if __name__ == "__main__":
    Checker().run(sys.argv[1:])
