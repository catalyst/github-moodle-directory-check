from app.moodle_plugin_directory_page import MoodlePluginDirectoryPage


class Repositories:
    def __init__(self, github, maintainer):
        self.github = github
        self.maintainer = maintainer
        self.skipped = None
        self.invalid = None
        self.unpublished = None
        self.thirdparty = None
        self.outdated = None
        self.uptodate = None

    def fetch(self):
        from app.checker import Checker
        Checker.debug('Fetching repositories on GitHub for: ' + self.github.owner)
        repositories = self.github.fetch_repositories()
        self.categorise_repositories(repositories)

    def categorise_repositories(self, repositories):
        from app.checker import Checker
        self.skipped = []
        self.invalid = []
        self.unpublished = []
        self.thirdparty = []
        self.outdated = []
        self.uptodate = []

        for repository in repositories:
            Checker.debug('Analysing: ' + repository.name)
            self.categorise_repository(repository)
        Checker.debug_end()

    def categorise_repository(self, repository):
        if not repository.has_moodle_repository_name():
            self.skipped.append(repository)
            return

        repository.fetch_github_metadata(self.github)
        if not repository.has_valid_github_metadata():
            self.invalid.append(repository)
            return

        directory = MoodlePluginDirectoryPage(repository.plugin)
        directory.fetch()
        if not directory.is_published():
            self.unpublished.append(repository)
            return

        if not directory.has_maintainer(self.maintainer):
            self.thirdparty.append(repository)
            return

        if not directory.has_version(repository.github_version):
            self.outdated.append(repository)
            return

        self.uptodate.append(repository)
