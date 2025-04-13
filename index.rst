..
    The :orphan: tag tells sphinx not to emit a warning that the index page is not referenced from
    any automatic table-of-contents.

:orphan:

Behat - a collaborative specification tool
==========================================


.. code-block:: gherkin

    Feature: Prove that software meets my business expectations
        In order to know when I have correctly implemented a feature
        As a PHP developer
        I want a tool to execute tests based on the agreed specifications

        Background:
          Given I have discussed a feature with the product team
          And   we have agreed a set of requirements in plain language

        Scenario: Work is complete
          Given I have correctly implemented the feature
          When  I run Behat with our specifications
          Then  I should see that the software behaves as expected


Behat is an open source `Behaviour Driven Development`_ tool for building software that
meets your business expectations.

It is the PHP implementation of `Cucumber`_, to execute specifications in **plain language**
that **anyone on your team** can read. This improves **communication**, **collaboration**
and **trust**, giving you the confidence to build the right system from the start and to
maintain it over time.

.. button::
   :text: Read the quick start guide
   :link: /quick_start.html
   :class: btn btn-lg btn-primary btn-block mb-1

.. button::
   :text: Explore the documentation
   :link: /guides.html
   :class: btn btn-lg btn-primary btn-block mb-1


Cover your whole application
----------------------------

Behat helps you to focus on business expectations and user-facing behaviour. This is
very different to many test runners, where tests become tied to implementations and
to individual layers of your stack.

With Behat, your feature files can describe the whole behaviour of your application.
You then have total freedom to decide how to implement the code that proves
the application works as expected.

This allows you to "mix and match" different testing approaches and technologies.
Browser automation; HTTP API calls; running shell commands; communicating directly
with your database, filesystem or PHP code: anything is possible.

You can even use profiles, tags and suites to test the same features in different ways.
For example, a quick regression test that directly calls your API handlers in PHP,
or a more thorough test over HTTP when you've made bigger changes. It's all up to you!

Built for PHP, for any framework
--------------------------------

Behat is a well structured PHP library designed for use with any framework (or none).
Internally, the codebase uses Symfony components, but you will find it easy to use in
any PHP project.

Behat provides flexible and developer-friendly interfaces for your tests, follows
modern coding standards and scores high ratings in static analysis tools.

And of course, all of `Behat's features are specified in plain language`_ and tested with Behat!


Extensible to the core
----------------------

Behat was built from the ground up to be extensible. Almost every part of Behat's functionality
can be enhanced or replaced through the extension system.

There are a wide range of `extensions`_ already available. These include integrations with
common PHP application frameworks, browser automation, test result reporters, data fixtures
and many more.

.. _`Behaviour Driven Development`: https://en.wikipedia.org/wiki/Behavior-driven_development
.. _`Cucumber`: https://cucumber.io/
.. _`Behat's features are specified in plain language`: https://github.com/Behat/Behat/tree/master/features
.. _`extensions`: https://github.com/search?o=desc&q=behat+extension+in%3Aname%2Cdescription&ref=searchresults&s=stars&type=Repositories&utf8=%E2%9C%93
