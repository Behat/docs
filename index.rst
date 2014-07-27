Behat Documentation
===================

Behat is an open source behavior-driven development framework for PHP 5.3 and 5.4.
What is *behavior-driven development*, you ask? It's the idea that you start
by writing human-readable sentences that describe a feature of your application
and how it should work, and only then implement this behavior in software.

For example, imagine you're about to create the famous UNIX ``ls`` command.
Before you begin, you describe how the feature should work:

.. code-block:: gherkin

    Feature: ls
      In order to see the directory structure
      As a UNIX user
      I need to be able to list the current directory's contents

      Scenario:
        Given I am in a directory "test"
        And I have a file named "foo"
        And I have a file named "bar"
        When I run "ls"
        Then I should get:
          """
          bar
          foo
          """

As a developer, your work is done as soon as you've made the ``ls`` command
behave as described in the *Scenario*.

Now, wouldn't it be cool if something could read this sentence and use it to
actually run a test against the ``ls`` command? Hey, that's exactly what Behat
does! As you'll see, Behat is easy to learn, quick to use, and will put the
fun back into your testing.

.. note::

    Behat was inspired by Ruby’s Cucumber project, especially its syntax
    (called Gherkin).

Quick Intro
-----------

To become *Behat'er* in 20 minutes, just dive into the quick-start guide and
enjoy!

.. toctree::
    :maxdepth: 2

    quick_intro

Guides
------

Learn Behat with the topical guides:

.. toctree::
    :maxdepth: 1

    guides/1.gherkin
    guides/2.definitions
    guides/3.hooks
    guides/4.context
    guides/5.closures
    guides/6.cli
    guides/7.config

Cookbook
--------

Learn specific solutions for specific needs:

.. toctree::
    :maxdepth: 1

    cookbook/behat_and_mink
    cookbook/migrate_from_1x_to_20
    cookbook/using_spin_functions

Useful Resources
----------------

Other useful resources for learning/using Behat:

* `Cheat Sheet <http://blog.lepine.pro/wp-content/uploads/2012/03/behat-cheat-sheet-en.pdf>`_
  - Behat and Mink Cheat Sheets by `Jean-François Lépine <http://blog.lepine.pro/>`_
* `Behat API <http://docs.behat.org/behat-api/>`_ - Behat code API
* `Gherkin API <http://docs.behat.org/gherkin-api/>`_ - Gherkin parser API

More about Behavior Driven Development
--------------------------------------

Once you're up and running with Behat, you can learn more about behavior-driven
development via the following links. Though both tutorials are specific to Cucumber,
Behat shares a lot with Cucumber and the philosophies are one
and the same.

* `Dan North's "What's in a Story?" <http://dannorth.net/whats-in-a-story/>`_
* `Cucumber's "Backgrounder" <https://github.com/cucumber/cucumber/wiki/Cucumber-Backgrounder>`_
