#!/usr/bin/env python3


class Repositories:
    def __init__(self):
        self.skipped = ['my-repository']
        self.invalid = ['moodle-not-a-plugin']
        self.outdated = ['moodle-local_updateme']
        self.updated = ['moodle-local_published']


class Checker:
    def run(self):
        repositories = Repositories()
        for group in ['skipped', 'invalid', 'outdated', 'updated']:
            for repository in getattr(repositories, group):
                print('{:>8}: {}'.format(group, repository))


if __name__ == "__main__":
    Checker().run()
