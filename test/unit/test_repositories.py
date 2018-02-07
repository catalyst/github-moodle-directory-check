import contextlib
import unittest
from io import StringIO

from app.checker import *


class CheckerTest(unittest.TestCase):

    def test_it_has_all_repository_groups(self):
        repositories = Repositories()
        self.assertIsNotNone(repositories.skipped)
        self.assertIsNotNone(repositories.invalid)
        self.assertIsNotNone(repositories.outdated)
        self.assertIsNotNone(repositories.updated)


