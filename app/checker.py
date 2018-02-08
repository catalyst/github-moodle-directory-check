#!/usr/bin/env python3
import re
from argparse import ArgumentParser

import sys

import requests
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


class Repository:
    def __init__(self, name):
        self.name = name

    def has_moodle_repository_name(self):
        return re.match(r"^moodle-.", self.name) is not None


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
        for repository in github.user_repositories(user):
            if not repository.has_moodle_repository_name():
                self.skipped.append(repository)
                continue
            if repository.name == 'moodle-not-a-plugin':
                self.invalid.append(repository)
                continue
            if repository.name == 'moodle-local_updateme':
                self.outdated.append(repository)
                continue
            self.updated.append(repository)


class GithubConnector:
    def __init__(self, token):
        self.github = Github(token)

    def user_repositories(self, username):
        for repository in self.github.get_user(username).get_repos():
            yield Repository(repository.name)

    def get_file(self, username, repository, file):
        link = "https://github.com/" + username + "/" + repository + "/raw/HEAD/" + file
        data = requests.get(link)
        return data.text


class Checker:
    @staticmethod
    def run(argv):
        arguments = CheckerArgumentParser(argv)
        repositories = Repositories()
        github = GithubConnector(arguments.token)
        repositories.fetch(github, arguments.user)
        for group in ['skipped', 'invalid', 'outdated', 'updated']:
            for repository in getattr(repositories, group):
                print('{:>8}: {}'.format(group, repository.name))


if __name__ == "__main__":
    Checker().run(sys.argv[1:])
