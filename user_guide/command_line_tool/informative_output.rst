Informative output
==================

.. _user-guide--comand-line-tool--informative-output--print-definitions:

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
