import requests
from pyquery import PyQuery


class MoodlePluginDirectoryPage:
    def __init__(self, plugin):
        self.plugin = plugin
        self.html = None
        self.pyquery = None

    def fetch(self):
        self.html = None
        self.pyquery = None
        url = "https://moodle.org/plugins/pluginversions.php?plugin=" + self.plugin
        data = requests.get(url)
        if data.status_code == 200:
            self.html = data.text
            self.pyquery = PyQuery(self.html)

    def has_maintainer(self, name):
        elements = self.pyquery('div.maintainedby span.name')
        for link in elements:
            if name == link.text:
                return True
        return False

    def has_version(self, version):
        elements = self.pyquery('div.versions-items h4 span.version')
        for div in elements:
            found = float(div.text.strip().rstrip(')').lstrip('('))
            if version == found:
                return True
        return False

    def is_published(self):
        return self.html is not None
