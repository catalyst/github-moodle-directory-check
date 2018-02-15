#!/usr/bin/env python3
import re
import sys
from argparse import ArgumentParser

import requests
from github import Github
from pyquery import PyQuery


class CheckerArgumentParser(ArgumentParser):
    def __init__(self, args):
        super().__init__()
        self.add_help = True
        self.add_argument('--token', help='GitHub Token', required=True)
        self.add_argument('--owner', help="Username of repositories' owner to check in GitHub", required=True)
        self.add_argument('--maintainer', help="Maintainer name on Moodle Plugin Directory", required=True)
        self.add_argument('--verbose', '-v', help="Show debugging information", action='store_true', default=False)
        self.add_argument('--quiet', '-q', help="Only display the results", action='store_true', default=False)
        args = self.parse_args(args)
        self.token = args.token
        self.owner = args.owner
        self.maintainer = args.maintainer
        self.verbose = args.verbose
        self.quiet = args.quiet


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
    def __init__(self, github, maintainer):
        self.github = github
        self.maintainer = maintainer
        self.skipped = None
        self.invalid = None
        self.unpublished = None
        self.thirdparty = None
        self.outdated = None
        self.uptodate = None

    def fetch(self):
        Checker.debug('Fetching repositories on GitHub for: ' + self.github.owner)
        repositories = self.github.fetch_repositories()
        self.categorise_repositories(repositories)

    def categorise_repositories(self, repositories):
        self.skipped = []
        self.invalid = []
        self.unpublished = []
        self.thirdparty = []
        self.outdated = []
        self.uptodate = []

        for repository in repositories:
            Checker.debug('Analysing: ' + repository.name)
            self.categorise_repository(repository)
        Checker.debug_end()

    def categorise_repository(self, repository):
        if not repository.has_moodle_repository_name():
            self.skipped.append(repository)
            return

        repository.fetch_github_metadata(self.github)
        if not repository.has_valid_github_metadata():
            self.invalid.append(repository)
            return

        directory = MoodlePluginDirectoryPage(repository.plugin)
        directory.fetch()
        if not directory.is_published():
            self.unpublished.append(repository)
            return

        if not directory.has_maintainer(self.maintainer):
            self.thirdparty.append(repository)
            return

        if not directory.has_version(repository.github_version):
            self.outdated.append(repository)
            return

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


class MoodlePluginDirectoryPage:
    def __init__(self, plugin):
        self.plugin = plugin
        self.html = None
        self.pyquery = None

    def fetch(self):
        self.html = None
        self.pyquery = None
        url = "https://moodle.org/plugins/pluginversions.php?plugin=" + self.plugin
        data = requests.get(url)
        if data.status_code == 200:
            self.html = data.text
            self.pyquery = PyQuery(self.html)

    def has_maintainer(self, name):
        elements = self.pyquery('div.maintainedby span.name')
        for link in elements:
            if name == link.text:
                return True
        return False

    def has_version(self, version):
        elements = self.pyquery('div.versions-items h4 span.version')
        for div in elements:
            found = float(div.text.strip().rstrip(')').lstrip('('))
            if version == found:
                return True
        return False

    def is_published(self):
        return self.html is not None


class Checker:
    show_dots = False
    show_debug = False

    @staticmethod
    def debug(message):
        if Checker.show_dots:
            print('.', end='')
        if Checker.show_debug:
            print(message, file=sys.stderr)

    @staticmethod
    def debug_end():
        if Checker.show_dots:
            print(end='\n\n')

    @staticmethod
    def run(argv):
        arguments = CheckerArgumentParser(argv)
        Checker.show_dots = not arguments.quiet and not arguments.verbose
        Checker.show_debug = not arguments.quiet and arguments.verbose
        github = GithubConnector(arguments.token, arguments.owner)
        repositories = Repositories(github, arguments.maintainer)
        repositories.fetch()
        for group in ['skipped', 'invalid', 'unpublished', 'thirdparty', 'outdated', 'uptodate']:
            for repository in getattr(repositories, group):
                print('{:>12}: {}'.format(group, repository.name))


if __name__ == "__main__":
    Checker().run(sys.argv[1:])