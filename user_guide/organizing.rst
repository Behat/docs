Organizing Features and Scenarios
=================================

.. _user-guide--organizing-features-and-scenarios--tags:

Tags
----

Tags are a great way to organize your features and scenarios. Consider this
example:

.. code-block:: gherkin

    @billing
    Feature: Verify billing

      @important
      Scenario: Missing product description

      Scenario: Several products

A Scenario or Feature can have as many tags as you like, just separate them
with spaces:

.. code-block:: gherkin

    @billing @bicker @annoy
    Feature: Verify billing

.. note::

    If a tag exists on a ``Feature``, Behat will assign that tag to all
    child ``Scenarios`` and ``Scenario Outlines`` too.