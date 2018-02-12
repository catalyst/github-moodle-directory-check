import os
from urllib import parse

from app.checker import Repository


class MockRequests:
    @staticmethod
    def get(url):
        if url == 'https://moodle.org/plugins/pluginversions.php?plugin=local_newplugin':
            return MockRequests(404, 'Not found')

        if url == 'https://moodle.org/plugins/pluginversions.php?plugin=auth_saml2':
            return MockRequests.fixture()

        if url == 'https://github.com/theowner/moodle-not-a-plugin/raw/HEAD/version.php':
            return MockRequests(404, 'Not found')

        if url == 'https://github.com/theowner/moodle-new-plugin/raw/HEAD/version.php':
            return MockRequests(200, '$plugin->version="2018021211.58";$plugin->component="local_newplugin";')

        if url == 'https://github.com/theowner/moodle-not-mine/raw/HEAD/version.php':
            return MockRequests(200, '$plugin->version="2018020915";$plugin->component="local_notmyplugin";')

        if url == 'https://github.com/theowner/moodle-local_updateme/raw/HEAD/version.php':
            return MockRequests(200, '$plugin->version="2018020814.43";$plugin->component="local_ninjaturtle";')

        if url == 'https://github.com/theowner/moodle-local_published/raw/HEAD/version.php':
            return MockRequests(200, '$plugin->version="2018020913.29";$plugin->component="local_ninjaturtle";')

        directory = [
            'https://moodle.org/plugins/pluginversions.php?plugin=local_notmyplugin',
            'https://moodle.org/plugins/pluginversions.php?plugin=local_ninjaturtle',
        ]
        if url in directory:
            return MockRequests.get_moodle_plugin_directory(url)

        raise Exception('Invalid MockRequests.get for: ' + url)

    @staticmethod
    def get_moodle_plugin_directory(url):
        query = parse.urlparse(url).query
        plugin = parse.parse_qs(query)['plugin'][0]
        (maintainer) = MockRequests.get_moodle_plugin_directory_data(plugin)
        maintainer = '<div class="maintainedby"><span class="name">{}</span></div>'.format(maintainer)
        return MockRequests(200, '<html>{}</html>'.format(maintainer))

    @staticmethod
    def get_moodle_plugin_directory_data(plugin):
        if plugin == 'local_notmyplugin':
            return 'Someone Else'
        if plugin == 'local_ninjaturtle':
            return 'Catalyst IT'
        raise Exception('Invalid MockRequests.get_moodle_plugin_directory_data for: ' + plugin)

    @staticmethod
    def fixture():
        file = os.path.dirname(__file__)
        file = os.path.join(file, '..', 'fixtures', 'auth_saml2.html')
        with open(file, 'r') as file:
            text = file.read()
        return MockRequests(200, text)

    def __init__(self, status, text):
        self.status_code = status
        self.text = text
