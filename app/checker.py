import sys

from app.checker_argument_parser import CheckerArgumentParser
from app.github_connector import GithubConnector
from app.repositories import Repositories


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
