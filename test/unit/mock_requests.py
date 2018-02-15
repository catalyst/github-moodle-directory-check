import os
import re


class MockRequests:
    @staticmethod
    def get(url):
        if url[:53] == 'https://moodle.org/plugins/pluginversions.php?plugin=':
            return MockRequests.get_moodle_plugin_directory(url[53:])

        matches = re.match(r'https://github.com/theowner/(.*)/raw/HEAD/version.php', url)
        if matches is not None:
            return MockRequests.get_github_versionphp(matches.group(1))

        raise Exception('Invalid MockRequests.get for: ' + url)

    @staticmethod
    def get_moodle_plugin_directory(plugin):
        if plugin == 'auth_saml2':
            return MockRequests.fixture(plugin + '.html')

        maintainer, version = MockRequests.get_moodle_plugin_directory_data(plugin)
        if maintainer is None or version is None:
            return MockRequests(404, 'Not found')

        maintainer = '<div class="maintainedby"><span class="name">{}</span></div>'.format(maintainer)
        version = '<div class="versions-items"><h4>XYZ <span class="version">({})</span></h4></div>'.format(version)
        return MockRequests(200, '<html>{}{}</html>'.format(maintainer, version))

    @staticmethod
    def get_moodle_plugin_directory_data(plugin):
        if plugin == 'local_newplugin':
            return None, None
        if plugin == 'local_notmyplugin':
            return 'Someone Else', '2018020910'
        if plugin == 'local_updateme':
            return 'The Maintainer', '2018010100'
        if plugin == 'local_published':
            return 'The Maintainer', '2018020913.29'
        if plugin == 'local_uptodateint':
            return 'The Maintainer', '2018021500'
        raise Exception('Invalid MockRequests.get_moodle_plugin_directory_data for: ' + plugin)

    @staticmethod
    def fixture(filename):
        file = os.path.dirname(__file__)
        file = os.path.join(file, '..', 'fixtures', filename)
        with open(file, 'r') as file:
            text = file.read()
        return MockRequests(200, text)

    def __init__(self, status, text):
        self.status_code = status
        self.text = text

    @staticmethod
    def get_github_versionphp(plugin):
        if plugin == 'moodle-not-a-plugin':
            return MockRequests(404, 'Not found')

        if plugin == 'moodle-new-plugin':
            return MockRequests(200, '$plugin->version="2018021211.58";$plugin->component="local_newplugin";')

        if plugin == 'moodle-not-mine':
            return MockRequests(200, '$plugin->version="2018020915";$plugin->component="local_notmyplugin";')

        if plugin == 'moodle-local_updateme':
            return MockRequests(200, '$plugin->version="2018020814.43";$plugin->component="local_updateme";')

        if plugin == 'moodle-local_published':
            return MockRequests(200, '$plugin->version="2018020913.29";$plugin->component="local_published";')

        if plugin == 'moodle-local_uptodateint':
            return MockRequests(200, '$plugin->version="2018021500";$plugin->component="local_uptodateint";')

        raise Exception('Invalid MockRequests.get_github_versionphp for: ' + plugin)
