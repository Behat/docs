Gherkin Compatibility Mode
==========================

Behat uses the `behat/gherkin`_ library to parse your feature files into the data structures that
Behat will use to execute them.

In most cases, this parses identically to `the official parsers provided by the Cucumber project`_.
However, there are some small differences in how our parser has traditionally treated some specific
syntax compared to the official parsers.

To resolve this, we have added a ``GherkinCompatibilityMode`` setting to the parser. This setting
has two possible options:

* ``GherkinCompatibilityMode::LEGACY`` - match our previous behaviour. This is the default in Behat 3.x.
* ``GherkinCompatibilityMode::GHERKIN_32`` - match the official parsers. This will become the default in Behat 4.0.

.. caution::
    ``GherkinCompatibilityMode::GHERKIN_32`` is currently considered experimental. We expect that
    there will be more changes to how the parser behaves in this mode before we mark it as stable.

Configuring the parser mode
---------------------------

In Behat >= 3.30, you can specify the parser compatibility mode for your project in
your :doc:`/user_guide/configuration`:

.. code-block:: php

    <?php
    use Behat\Config\GherkinOptions;
    use Behat\Config\Profile;
    use Behat\Gherkin\GherkinCompatibilityMode;

    return new Config()
       ->withProfile(new Profile('default')
           ->withGherkinOptions(new GherkinOptions()
              ->withCompatibilityMode(GherkinCompatibilityMode::GHERKIN_32)
           )
       )
    ;

Differences between parser modes
--------------------------------

Tables containing whitespace or escaped newlines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``GHERKIN_32`` mode, table cells can include newlines, which will be unescaped during parsing. Note that
newlines are unescaped **after** we remove the cell padding.

For example, with the following table:

.. code-block:: gherkin

    Given 3 lines of poetry on 5 lines:
      | \nraindrops--\nher last kiss\ngoodbye.\n  |

In ``GHERKIN_32`` mode, the table will parse as:

.. code-block:: php

    [
      [
          <<<TEXT

          raindrops--
          her last kiss
          goodbye.

          TEXT
      ]
    ]

In legacy mode, this would be parsed as ``'\nraindrops--\nher last kiss\ngoodbye.'``.

The other difference is in how the parser trims padding of table cells:

* In ``GHERKIN_32`` mode, all leading and trailing whitespace, including tabs and unicode whitespace, is removed.
* In ``LEGACY`` mode, only literal space characters are removed.


Docstrings
~~~~~~~~~~

Docstrings (which Behat has historically referred to as PyStrings) in feature files can contain escaped delimiters -
for example:

.. code-block:: gherkin

    And a DocString with escaped separator inside
      """
      first line
      \"\"\"
      third line
      """

In ``GHERKIN_32`` mode, the parser will unescape the delimiters - e.g. this will be parsed as:

.. code-block:: text

    first line
    """
    third line

In legacy mode, the parsed string is not unescaped - e.g. it includes the literal ``\"\"\"`` text.

Parsing of tags
~~~~~~~~~~~~~~~

In ``GHERKIN_32`` mode:

* Parsing fails if any tags contain whitespace (e.g. ``@some tag``). In legacy mode, these have triggered
  an ``E_USER_DEPRECATED`` since behat/gherkin v4.9.0
* The values returned by ``$node->getTags()`` will **include** the ``@`` prefix. In legacy mode,
  this was removed. This may affect custom hooks / event listeners that inspect the tag values at
  runtime.


File language
~~~~~~~~~~~~~

In ``GHERKIN_32`` mode, if a file includes a ``#language`` annotation:

* Any whitespace in / around the tag will be ignored - so ``# language : fr`` will be
  recognised as a valid language tag. In legacy mode, this would have been treated as a comment.
* Parsing fails if the language is not recognised - so ``#language: no-such`` will cause an error.
  In legacy mode, this would have been ignored and parsing would continue in the default language.

Whitespace following step keywords
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``GHERKIN_32`` mode, a space between a step keyword and the rest of the text is treated as part of the keyword. This
is because in a small number of languages there is no space after the keyword.

With a step in English like ``Then something should happen``, if you call ``StepNode::getKeyword()`` then:

* In ``GHERKIN_32`` mode the return value will be ``'Then '``
* In ``LEGACY`` mode the return value will be ``'Then'``

In a language that does not place spaces after the keyword (e.g. Japanese), the return value will be the same in both
modes.

Elements with descriptions
~~~~~~~~~~~~~~~~~~~~~~~~~~

Gherkin syntax allows multi-line descriptions on ``Feature:``, ``Background:``, ``Scenario:``, ``Scenario Outline:``,
and ``Examples:`` elements.

Historically, we only parsed the description separately for a ``Feature`` node. For other nodes, we parsed the full
text as a multi-line title.

In ``GHERKIN_32`` mode, if one of the elements listed above has multi-line text, then:

* The first line (containing the keyword) will be parsed as the title.
* Following lines will be parsed as the description.
* Any blank lines between the title & description will be ignored (in legacy mode, these were included at the start of
  the description).
* Any left padding will be removed from the first line of the description, but subsequent lines will have the same
  left padding / indentation as the feature file. In legacy mode, we attempted to left-trim all lines to match the
  indentation of the keyword.


.. _`behat/gherkin`: http://martinfowler.com/bliki/BusinessReadableDSL.html
.. _`the official parsers provided by the Cucumber project`: https://github.com/cucumber/gherkin
