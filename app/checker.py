#!/usr/bin/env python3
import re
import sys
from argparse import ArgumentParser

import requests
from github import Github


class CheckerArgumentParser(ArgumentParser):
    def __init__(self, args):
        super().__init__()
        self.add_help = True
        self.add_argument('--token', help='GitHub Token', required=True)
        self.add_argument('--owner', help="Username of repositories' owner to check in GitHub", required=True)
        args = self.parse_args(args)
        self.token = args.token
        self.owner = args.owner


class Repository:
    def __init__(self, name):
        self.name = name
        self.plugin = None
        self.github_version = None

    def has_moodle_repository_name(self):
        return re.match(r"^moodle-.", self.name) is not None

    def fetch_github_metadata(self, github):
        self.plugin = None
        self.github_version = None
        html = github.get_file(self.name, 'version.php')
        if html is None:
            return
        match = re.search(r"\$plugin->version[\s]*=[\s]*['\"]?([\d\\.]+)['\"]?[\s]*;", html)
        if match is not None:
            self.github_version = float(match.group(1))
        match = re.search(r"\$plugin->component[\s]*=[\s]*['\"]([\w\\.]+)['\"][\s]*;", html)
        if match is not None:
            self.plugin = match.group(1)

    def has_valid_github_metadata(self):
        if self.plugin is None:
            return False
        if self.github_version is None:
            return False
        return True


class Repositories:
    def __init__(self, github):
        self.github = github
        self.skipped = None
        self.invalid = None
        self.thirdparty = None
        self.outdated = None
        self.uptodate = None

    def fetch(self):
        repositories = self.github.fetch_repositories()
        self.categorise_repositories(repositories)

    def categorise_repositories(self, repositories):
        self.skipped = []
        self.invalid = []
        self.thirdparty = []
        self.outdated = []
        self.uptodate = []
        for repository in repositories:
            if not repository.has_moodle_repository_name():
                self.skipped.append(repository)
                continue
            repository.fetch_github_metadata(self.github)
            if not repository.has_valid_github_metadata():
                self.invalid.append(repository)
                continue
            if repository.name == 'moodle-not-mine':
                self.thirdparty.append(repository)
                continue
            if repository.name == 'moodle-local_updateme':
                self.outdated.append(repository)
                continue
            self.uptodate.append(repository)


class GithubConnector:
    def __init__(self, token, repository_owner):
        self.github = Github(token)
        self.owner = repository_owner

    def fetch_repositories(self):
        for repository in self.github.get_user(self.owner).get_repos():
            yield Repository(repository.name)

    def get_file(self, repository, file):
        link = "https://github.com/" + self.owner + "/" + repository + "/raw/HEAD/" + file
        data = requests.get(link)
        if data.status_code != 200:
            return None
        return data.text


class Checker:
    @staticmethod
    def run(argv):
        arguments = CheckerArgumentParser(argv)
        github = GithubConnector(arguments.token, arguments.owner)
        repositories = Repositories(github)
        repositories.fetch()
        for group in ['skipped', 'invalid', 'thirdparty', 'outdated', 'uptodate']:
            for repository in getattr(repositories, group):
                print('{:>10}: {}'.format(group, repository.name))


if __name__ == "__main__":
    Checker().run(sys.argv[1:])
