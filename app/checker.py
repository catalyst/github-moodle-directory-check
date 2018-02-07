#!/usr/bin/env python3
from github import Github


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
    def run(self):
        repositories = Repositories()
        for group in ['skipped', 'invalid', 'outdated', 'updated']:
            for repository in getattr(repositories, group):
                print('{:>8}: {}'.format(group, repository))


if __name__ == "__main__":
    Checker().run()
