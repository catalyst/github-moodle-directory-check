import re


class RepositoryChecker(object):

    def is_moodle_repository(self, name):
        return re.match(r"^moodle-.", name) is not None
