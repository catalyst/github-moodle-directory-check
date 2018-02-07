class Repositories:
    def __init__(self):
        self.skipped = ['my-repository']
        self.invalid = ['moodle-not-a-plugin']
        self.outdated = ['moodle-local_updateme']
        self.updated = ['moodle-local_published']


class Checker:
    def run(self):
        repositories = Repositories()
        for repository in repositories.skipped:
            print(' skipped: ' + repository)
        for repository in repositories.invalid:
            print(' invalid: ' + repository)
        for repository in repositories.outdated:
            print('outdated: ' + repository)
        for repository in repositories.updated:
            print(' updated: ' + repository)


if __name__ == "__main__":
    Checker().run()
