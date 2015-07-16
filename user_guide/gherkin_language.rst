About Gherkin Language
======================

Behat is a tool to test the behavior of your application, described in a special
language called Gherkin. Gherkin is a
`Business Readable, Domain Specific Language`_
created specifically for behavior descriptions. It gives you the ability to
remove logic details from behavior tests.

Gherkin serves as your project's documentation as well as your project's
automated tests. Behat also has a bonus feature: It talks back to you using
real, human language telling you what code you should write.

.. tip::

    If you're still new to Behat, jump into the :doc:`/quick_start` first,
    then return here to learn more about Gherkin.

Gherkin Syntax
--------------

Like YAML and Python, Gherkin is a whitespace-oriented language that uses
indentation to define structure. Line endings terminate statements (called
steps) and either spaces or tabs may be used for indentation (we suggest you
use spaces for portability). Finally, most lines in Gherkin start with a
special keyword:

.. code-block:: gherkin

    Feature: Some terse yet descriptive text of what is desired
      In order to realize a named business value
      As an explicit system actor
      I want to gain some beneficial outcome which furthers the goal

      Additional text...

      Scenario: Some determinable business situation
        Given some precondition
        And some other precondition
        When some action by the actor
        And some other action
        And yet another action
        Then some testable outcome is achieved
        And something else we can check happens too

      Scenario: A different situation
        ...

The parser divides the input into features, scenarios and steps. Let's walk
through the above example:

#. ``Feature: Some terse yet descriptive text of what is desired`` starts
   the feature and gives it a title. Learn more about ":ref:`user-guide--features-scenarios--features`".

#. The next three lines (``In order to ...``, ``As an ...``, ``I want to
   ...``) provide context to the people reading your feature and describe the
   business value derived from the inclusion of the feature in your software.
   These lines are not parsed by Behat and don't have a required structure.

#. ``Scenario: Some determinable business situation`` starts the scenario
   and contains a description of the scenario. Learn more about
   ":ref:`user-guide--features-scenarios--scenarios`".

#. The next 7 lines are the scenario steps, each of which is matched to
   a pattern defined elsewhere. Learn more about
   ":ref:`user-guide--writing-scenarios--steps`".

#. ``Scenario: A different situation`` starts the next scenario and so on.

When you're executing the feature, the trailing portion of each step (after
keywords like ``Given``, ``And``, ``When``, etc) is matched to
a pattern, which executes a PHP callback function. You can read more about
steps matching and execution in ":doc:`/user_guide/feature_contexts/defining_step_definitions`".

Gherkin in Many Languages
-------------------------

Gherkin is available in many languages, allowing you to write stories
using localized keywords from your language. In other words, if you
speak French, you can use the word ``Fonctionnalité`` instead of ``Feature``.

To check if Behat and Gherkin support your language (for example, French),
run:

.. code-block:: bash

    behat --story-syntax --lang=fr

.. note::

    Keep in mind that any language different from ``en`` should be explicitly
    marked with a ``# language: ...`` comment at the beginning of your
    ``*.feature`` file:

    .. code-block:: gherkin

        # language: fr
        Fonctionnalité: ...
          ...

    This way your features will hold all the information about its content
    type, which is very important for methodologies like BDD and also gives
    Behat the ability to have multilanguage features in one suite.

.. _`Business Readable, Domain Specific Language`: http://martinfowler.com/bliki/BusinessReadableDSL.html