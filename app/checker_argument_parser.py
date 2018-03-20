from argparse import ArgumentParser


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
