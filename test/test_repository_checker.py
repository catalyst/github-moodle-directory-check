import unittest
from app.repository_checker import RepositoryChecker


class RepositoryCheckerTest(unittest.TestCase):

    def test_it_detects_correct_repositories(self):
        checker = RepositoryChecker()
        self.assertFalse(checker.is_moodle_repository(''))
        self.assertFalse(checker.is_moodle_repository('moodle-'))
        self.assertTrue(checker.is_moodle_repository('moodle-something'))
