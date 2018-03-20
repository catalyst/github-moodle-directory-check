import unittest

from app.checker_argument_parser import CheckerArgumentParser


class CheckerArgumentParserTest(unittest.TestCase):

    def test_it_parses_the_parameters(self):
        parser = CheckerArgumentParser(['--token', 'abcd', '--owner', 'someone', '--maintainer', 'Daniel Roperto'])
        self.assertEquals("abcd", parser.token)
        self.assertEquals('someone', parser.owner)
        self.assertEquals('Daniel Roperto', parser.maintainer)
        self.assertFalse(parser.verbose)
        self.assertFalse(parser.quiet)

    def test_it_parses_the_parameters_with_verbose(self):
        parser = CheckerArgumentParser(['--token', 'a', '--owner', 'o', '--maintainer', 'm', '-v'])
        self.assertTrue(parser.verbose)

    def test_it_parses_the_parameters_with_quiet(self):
        parser = CheckerArgumentParser(['--token', 'a', '--owner', 'o', '--maintainer', 'm', '-q'])
        self.assertTrue(parser.quiet)
