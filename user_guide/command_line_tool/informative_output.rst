Informative Output
==================

.. _user-guide--command-line-tool--informative-output--print-definitions:

Print Definitions
-----------------

As your set of features will grow, there's a good chance that the amount of
different steps that you'll have at your disposal to describe new scenarios will also grow.

Behat provides a command line option ``--definitions`` or simply ``-d`` to easily browse definitions
in order to reuse them or adapt them (introducing new placeholders for example).

For example, when using the Mink context provided by the Mink extension, you'll have access to its
step dictionary by running:

.. code-block:: console

    $ behat -di
    web_features | Given /^(?:|I )am on (?:|the )homepage$/
                 | Opens homepage.
                 | at `Behat\MinkExtension\Context\MinkContext::iAmOnHomepage()`

    web_features | When /^(?:|I )go to (?:|the )homepage$/
                 | Opens homepage.
                 | at `Behat\MinkExtension\Context\MinkContext::iAmOnHomepage()`

    web_features | Given /^(?:|I )am on "(?P<page>[^"]+)"$/
                 | Opens specified page.
                 | at `Behat\MinkExtension\Context\MinkContext::visit()`

    # ...

or, for a shorter output:

.. code-block:: console

    $ behat -dl
    web_features | Given /^(?:|I )am on (?:|the )homepage$/
    web_features |  When /^(?:|I )go to (?:|the )homepage$/
    web_features | Given /^(?:|I )am on "(?P<page>[^"]+)"$/
    web_features |  When /^(?:|I )go to "(?P<page>[^"]+)"$/
    web_features |  When /^(?:|I )reload the page$/
    web_features |  When /^(?:|I )move backward one page$/
    web_features |  When /^(?:|I )move forward one page$/
    # ...

You can also search for a specific pattern by running:

.. code-block:: console

    $ behat --definitions="field" (or simply behat -dfield)
    web_features | When /^(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with "(?P<value>(?:[^"]|\\")*)"$/
                 | Fills in form field with specified id|name|label|value.
                 | at `Behat\MinkExtension\Context\MinkContext::fillField()`

    web_features | When /^(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with:$/
                 | Fills in form field with specified id|name|label|value.
                 | at `Behat\MinkExtension\Context\MinkContext::fillField()`

    #...

That's it, you can now search and browse your whole step dictionary.

Print Unused Definitions
------------------------

If your project is large, you may end up with definitions which are no longer used. If you want to print a list of
these unused definitions you can use the ``--print-unused-definitions`` command line flag. With this flag you will see
output similar to this:

.. code-block:: console

    $ behat --print-unused-definitions
      ...
      --- 1 unused definition:

      [Then|*] I call a step not used in any feature
      `FeatureContext::stepNotUsedInAnyFeature()`

This can also be set for each profile using the PHP configuration:

.. code-block:: php

    use Behat\Config\Config;
    use Behat\Config\Profile;

    return (new Config())
        ->withProfile(
            (new Profile('default'))
            ->withPrintUnusedDefinitions()
        )
    ;

Or the yaml configuration:

.. code-block:: yaml

    default:
        definitions:
            print_unused_definitions: true


