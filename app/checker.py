class Checker:
    def run(self):
        print(' skipped: my-repository')
        print(' invalid: moodle-not-a-plugin')
        print('outdated: moodle-local_updateme')
        print('      ok: moodle-local_published')


if __name__ == "__main__":
    Checker().run()
