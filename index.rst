Behat Documentation
===================

Behat is an open source Behavior Driven Development framework for PHP 5.3+.
What's *behavior driven development*, you ask? It's a way to develop software
through a constant communication with stakeholders in form of examples;
examples of how this software should help them, and you, to achieve your goals.

For example, imagine you're about to create the famous UNIX ``ls`` command.
Before you begin, you will have a conversation with your stakeholders (UNIX
users) and they might say that even though they like UNIX a lot, they need a
way to see all the files in the current working directory. You then have
a back-and-forth chat with them about how they see this feature
working and you come up with your first scenario (an alternative name for example
in BDD methodology):

.. code-block:: gherkin

    Feature: Listing command
      In order to change the structure of the folder I am currently in
      As a UNIX user
      I need to be able see the currently available files and folders there

      Scenario: Listing two files in a directory
        Given I am in a directory "test"
        And I have a file named "foo"
        And I have a file named "bar"
        When I run "ls"
        Then I should get:
          """
          bar
          foo
          """

If you are a stakeholder, this is your proof that developers understand
exactly how you want this feature to work. If you are a developer, this is your
proof that the stakeholder expects you to implement this feature exactly in the
way you're planning to implement it.

So, as a developer your work is done as soon as you've made the ``ls``
command, and made it behave as described in the "Listing command" scenario.

You've probably heard about this modern development practice called TDD, where
you write tests for your code before, not after, the code. Well, BDD is like
that, except that you don't need to come up with a test - your *scenarios* are
your tests. That's exactly what Behat does! As you'll see, Behat is easy to
learn, quick to use, and will put the fun back into your testing.

.. note::

    Behat was heavily inspired by Ruby's `Cucumber`_ project. Since v3.0,
    Behat is considered an official Cucumber implementation in PHP and is part
    of one big family of BDD tools.

.. toctree::
   :hidden:
   :maxdepth: 2

   intro
   quick_start
   user_guide
   cookbooks
   useful_resources

.. _`Cucumber`: http://cukes.info/