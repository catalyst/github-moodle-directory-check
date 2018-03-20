import re


class Repository:
    def __init__(self, name):
        self.name = name
        self.plugin = None
        self.github_version = None

    def has_moodle_repository_name(self):
        return re.match(r"^moodle-.", self.name) is not None

    def fetch_github_metadata(self, github):
        self.plugin = None
        self.github_version = None
        html = github.get_file(self.name, 'version.php')
        if html is None:
            return
        match = re.search(r"\$plugin->version[\s]*=[\s]*['\"]?([\d\\.]+)['\"]?[\s]*;", html)
        if match is not None:
            self.github_version = float(match.group(1))
        match = re.search(r"\$plugin->component[\s]*=[\s]*['\"]([\w\\.]+)['\"][\s]*;", html)
        if match is not None:
            self.plugin = match.group(1)

    def has_valid_github_metadata(self):
        if self.plugin is None:
            return False
        if self.github_version is None:
            return False
        return True
