import unittest
from unittest.mock import patch

from app.checker import *


class RepositoryTest(unittest.TestCase):

    def test_it_detects_correct_repository_names(self):
        self.assertFalse(Repository('').has_moodle_repository_name())
        self.assertFalse(Repository('moodle-').has_moodle_repository_name())
        self.assertTrue( Repository('moodle-something').has_moodle_repository_name())
