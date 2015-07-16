Features and Scenarios
======================

.. _user-guide--features-scenarios--features:

Features
--------

Every ``*.feature`` file conventionally consists of a single feature. Lines
starting with the keyword ``Feature:`` (or its localized equivalent) followed
by three indented lines starts a feature. A feature usually contains a list of
scenarios. You can write whatever you want up until the first scenario, which
starts with ``Scenario:`` (or localized equivalent) on a new line. You can use
:ref:`user-guide--organizing-features-and-scenarios--tags` to group features
and scenarios together, independent of your file and directory structure.

Every scenario consists of a list of
:ref:`user-guide--writing-scenarios--steps`, which must start with one of the
keywords ``Given``, ``When``, ``Then``, ``But`` or ``And`` (or a localized
version of one of these). Behat treats them all the same, but you shouldn't.
Here is an example:

.. code-block:: gherkin

    Feature: Serve coffee
      In order to earn money
      Customers should be able to
      buy coffee at all times

      Scenario: Buy last coffee
        Given there are 1 coffees left in the machine
        And I have deposited 1 dollar
        When I press the coffee button
        Then I should be served a coffee

In addition to basic :ref:`user-guide--features-scenarios--scenarios`,
features may contain :ref:`user-guide--writing-scenarios--scenario-outlines` and
:ref:`user-guide--writing-scenarios--backgrounds`.

.. _user-guide--features-scenarios--scenarios:

Scenarios
---------

Scenarios are one of the core Gherkin structures. Every scenario starts with
the ``Scenario:`` keyword (or localized keyword), followed by an optional scenario
title. Each feature can have one or more scenarios and every scenario consists
of one or more :ref:`user-guide--writing-scenarios--steps`.

The following scenarios each have 3 steps:

.. code-block:: gherkin

    Scenario: Wilson posts to his own blog
      Given I am logged in as Wilson
      When I try to post to "Expensive Therapy"
      Then I should see "Your article was published."

    Scenario: Wilson fails to post to somebody else's blog
      Given I am logged in as Wilson
      When I try to post to "Greg's anti-tax rants"
      Then I should see "Hey! That's not your blog!"

    Scenario: Greg posts to a client's blog
      Given I am logged in as Greg
      When I try to post to "Expensive Therapy"
      Then I should see "Your article was published."
