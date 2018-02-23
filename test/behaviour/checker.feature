Feature: Use checker to find the statuses of our plugins on GitHub

  Scenario: run a simple test
    Given the user "theowner" on GitHub has the following repositories:
      | Repository             |
      | my-repository          |
      | moodle-not-a-plugin    |
      | moodle-new-plugin      |
      | moodle-not-mine        |
      | moodle-local_updateme  |
      | moodle-local_published |
    When I run "checker.py --token thetoken --owner theowner --maintainer 'The Maintainer' -q"
    Then the output should be:
      """
           skipped: my-repository
           invalid: moodle-not-a-plugin
       unpublished: moodle-new-plugin
        thirdparty: moodle-not-mine
          outdated: moodle-local_updateme
          uptodate: moodle-local_published
      """
    And the error output should be empty