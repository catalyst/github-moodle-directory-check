import unittest

from app.checker import *


class CheckerArgumentParserTest(unittest.TestCase):

    def test_it_parses_the_parameters(self):
        parser = CheckerArgumentParser(['--token', 'abcd', '--owner', 'someone'])
        self.assertEquals("abcd", parser.token)
        self.assertEquals('someone', parser.owner)
