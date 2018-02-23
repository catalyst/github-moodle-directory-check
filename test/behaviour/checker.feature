Feature: Use checker to find the statuses of our plugins on GitHub

  Background:
    Given the user "theowner" on GitHub has the following repositories:
      | Repository             |
      | my-repository          |
      | moodle-not-a-plugin    |
      | moodle-new-plugin      |
      | moodle-not-mine        |
      | moodle-local_updateme  |
      | moodle-local_published |


  Scenario: Run checker without parameters should display the help
    When I run "checker.py"
    Then the output should be empty
    And the error output should contain "the following arguments are required: --token, --owner, --maintainer"

  Scenario: Run checker should show results with dots for progress
    When I run "checker.py --token thetoken --owner theowner --maintainer 'The Maintainer'"
    Then the output should be:
      """
      .......

           skipped: my-repository
           invalid: moodle-not-a-plugin
       unpublished: moodle-new-plugin
        thirdparty: moodle-not-mine
          outdated: moodle-local_updateme
          uptodate: moodle-local_published
      """
    And the error output should be empty

  Scenario: Running in quiet mode should show only the results
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

  Scenario: Running in verbose mode should show some extra information
    When I run "checker.py --token thetoken --owner theowner --maintainer 'The Maintainer' -v"
    Then the output should be:
      """
           skipped: my-repository
           invalid: moodle-not-a-plugin
       unpublished: moodle-new-plugin
        thirdparty: moodle-not-mine
          outdated: moodle-local_updateme
          uptodate: moodle-local_published
      """
    And the error output should be:
      """
      Fetching repositories on GitHub for: theowner
      Analysing: my-repository
      Analysing: moodle-not-a-plugin
      Analysing: moodle-new-plugin
      Analysing: moodle-not-mine
      Analysing: moodle-local_updateme
      Analysing: moodle-local_published
      """