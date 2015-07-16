Writing Scenarios
=================

.. _user-guide--writing-scenarios--steps:

Steps
-----

:ref:`user-guide--features-scenarios--features` consist of steps, also known as
`Givens`_, `Whens`_ and `Thens`_.

Behat doesn't technically distinguish between these three kind of steps.
However, we strongly recommend that you do! These words have been carefully
selected for their purpose and you should know what the purpose is to get into
the BDD mindset.

Robert C. Martin has written a `great post`_ about BDD's Given-When-Then concept
where he thinks of them as a finite state machine.

Givens
^^^^^^

The purpose of the **Given** steps is to **put the system in a known state** before
the user (or external system) starts interacting with the system (in the When
steps). Avoid talking about user interaction in givens. If you have worked with
use cases, givens are your preconditions.

.. sidebar:: Given Examples

    Two good examples of using **Givens** are:

    * To create records (model instances) or set up the database:

      .. code-block:: gherkin

          Given there are no users on site
          Given the database is clean

    * Authenticate a user (an exception to the no-interaction recommendation.
      Things that "happened earlier" are ok):

      .. code-block:: gherkin

          Given I am logged in as "Everzet"

.. tip::

    It's OK to call into the layer "inside" the UI layer here (in Symfony: talk
    to the models).

.. sidebar:: Using Givens as Data Fixtures

    If you use ORMs like Doctrine or Propel, we recommend using a Given step
    with a `tables`_ argument to   set up records instead of fixtures. This
    way you can read the scenario all in one place and make sense out of it
    without having to jump between files:

    .. code-block:: gherkin

        Given there are users:
        | username | password | email               |
        | everzet  | 123456   | everzet@knplabs.com |
        | fabpot   | 22@222   | fabpot@symfony.com  |

Whens
^^^^^

The purpose of **When** steps is to **describe the key action** the user
performs (or, using Robert C. Martin's metaphor, the state transition).

.. sidebar:: When Examples

    Two good examples of using **Whens** are:

    * Interact with a web page (the Mink library gives you many web-friendly
      ``When`` steps out of the box):

      .. code-block:: gherkin

          When I am on "/some/page"
          When I fill "username" with "everzet"
          When I fill "password" with "123456"
          When I press "login"

    * Interact with some CLI library (call commands and record output):

      .. code-block:: gherkin

          When I call "ls -la"

Thens
^^^^^

The purpose of **Then** steps is to **observe outcomes**. The observations
should be related to the business value/benefit in your feature description.
The observations should inspect the output of the system (a report, user
interface, message, command output) and not something deeply buried inside it
(that has no business value and is instead part of the implementation).

.. sidebar:: Then Examples

    Two good examples of using **Thens** are:

    * Verify that something related to the Given + When is (or is not) in the
      output:

      .. code-block:: gherkin

          When I call "echo hello"
          Then the output should be "hello"

    * Check that some external system has received the expected message:

      .. code-block:: gherkin

          When I send an email with:
            """
            ...
            """
          Then the client should receive the email with:
            """
            ...
            """

.. caution::

    While it might be tempting to implement Then steps to just look in the
    database – resist the temptation. You should only verify output that is
    observable by the user (or external system). Database data itself is
    only visible internally to your application, but is then finally exposed
    by the output of your system in a web browser, on the command-line or an
    email message.


And & But
^^^^^^^^^

If you have several Given, When or Then steps you can write:

.. code-block:: gherkin

    Scenario: Multiple Givens
      Given one thing
      Given another thing
      Given yet another thing
      When I open my eyes
      Then I see something
      Then I don't see something else

Or you can use **And** or **But** steps, allowing your Scenario to read more
fluently:

.. code-block:: gherkin

    Scenario: Multiple Givens
      Given one thing
      And another thing
      And yet another thing
      When I open my eyes
      Then I see something
      But I don't see something else

Behat interprets steps beginning with And or But exactly the same as all other
steps; it doesn't differentiate between them - you should!

.. _user-guide--writing-scenarios--backgrounds:

Backgrounds
-----------

Backgrounds allows you to add some context to all scenarios in a single
feature. A Background is like an untitled scenario, containing a number of
steps. The difference is when it is run: the background is run *before each* of
your scenarios, but after your ``BeforeScenario``
:ref:`user-guide--feature-contexts--hooking-into-the-test-process--hooks`.

.. code-block:: gherkin

    Feature: Multiple site support

      Background:
        Given a global administrator named "Greg"
        And a blog named "Greg's anti-tax rants"
        And a customer named "Wilson"
        And a blog named "Expensive Therapy" owned by "Wilson"

      Scenario: Wilson posts to his own blog
        Given I am logged in as Wilson
        When I try to post to "Expensive Therapy"
        Then I should see "Your article was published."

      Scenario: Greg posts to a client's blog
        Given I am logged in as Greg
        When I try to post to "Expensive Therapy"
        Then I should see "Your article was published."

.. _user-guide--writing-scenarios--scenario-outlines:

Scenario Outlines
-----------------

Copying and pasting scenarios to use different values can quickly become
tedious and repetitive:

.. code-block:: gherkin

    Scenario: Eat 5 out of 12
      Given there are 12 cucumbers
      When I eat 5 cucumbers
      Then I should have 7 cucumbers

    Scenario: Eat 5 out of 20
      Given there are 20 cucumbers
      When I eat 5 cucumbers
      Then I should have 15 cucumbers

Scenario Outlines allow us to more concisely express these examples through the
use of a template with placeholders:

.. code-block:: gherkin

    Scenario Outline: Eating
      Given there are <start> cucumbers
      When I eat <eat> cucumbers
      Then I should have <left> cucumbers

      Examples:
        | start | eat | left |
        |  12   |  5  |  7   |
        |  20   |  5  |  15  |

The Scenario Outline steps provide a template which is never directly run. A
Scenario Outline is run once for each row in the Examples section beneath it
(except for the first header row).

The Scenario Outline uses placeholders, which are contained within
``< >`` in the Scenario Outline's steps. For example:

.. code-block:: gherkin

    Given <I'm a placeholder and I'm ok>

Think of a placeholder like a variable. It is replaced with a real value from
the ``Examples:`` table row, where the text between the placeholder angle
brackets matches that of the table column header. The value substituted for
the placeholder changes with each subsequent run of the Scenario Outline,
until the end of the ``Examples`` table is reached.

.. tip::

    You can also use placeholders in `Multiline Arguments`_.

.. note::

    Your step definitions will never have to match the placeholder text itself,
    but rather the values replacing the placeholder.

So when running the first row of our example:

.. code-block:: gherkin

    Scenario Outline: Eating
      Given there are <start> cucumbers
      When I eat <eat> cucumbers
      Then I should have <left> cucumbers

      Examples:
        | start | eat | left |
        |  12   |  5  |  7   |

The scenario that is actually run is:

.. code-block:: gherkin

    Scenario: Eating
      # <start> replaced with 12:
      Given there are 12 cucumbers
      # <eat> replaced with 5:
      When I eat 5 cucumbers
      # <left> replaced with 7:
      Then I should have 7 cucumbers

Tables
------

Tables as arguments to steps are handy for specifying a larger data set -
usually as input to a Given or as expected output from a Then.

.. code-block:: gherkin

    Scenario:
      Given the following people exist:
        | name  | email           | phone |
        | Aslak | aslak@email.com | 123   |
        | Joe   | joe@email.com   | 234   |
        | Bryan | bryan@email.org | 456   |

.. attention::

    Don't confuse tables with `scenario outlines`_ - syntactically
    they are identical, but they have a different purpose. Outlines declare
    multiple different values for the same scenario, while tables are used to
    expect a set of data.

.. sidebar:: Matching Tables in your Step Definition

    A matching definition for this step looks like this:

    .. code-block:: php

        use Behat\Gherkin\Node\TableNode;

        // ...

        /**
         * @Given the following people exist:
         */
        public function thePeopleExist(TableNode $table)
        {
            foreach ($table as $row) {
                // $row['name'], $row['email'], $row['phone']
            }
        }

    A table is injected into a definition as a ``TableNode`` object, from
    which you can get hash by columns (``TableNode::getHash()`` method) or by
    rows (``TableNode::getRowsHash()``).

Multiline Arguments
-------------------

The one line `steps`_ let Behat extract small strings from your steps
and receive them in your step definitions. However, there are times when you
want to pass a richer data structure from a step to a step definition.

This is what multiline step arguments are designed for. They are written on
lines immediately following a step and are passed to the step definition
method as the last argument.

Multiline step arguments come in two flavours: `tables`_ or `pystrings`_.

Pystrings
---------

Multiline Strings (also known as PyStrings) are useful for specifying a
larger piece of text. The text should be offset by delimiters consisting of
three double-quote marks (``"""``), placed on their own line:

.. code-block:: gherkin

    Scenario:
      Given a blog post named "Random" with:
        """
        Some Title, Eh?
        ===============
        Here is the first paragraph of my blog post.
        Lorem ipsum dolor sit amet, consectetur adipiscing
        elit.
        """

.. note::

    The inspiration for PyString comes from Python where ``"""`` is used to
    delineate docstrings, much in the way ``/** ... */`` is used for multiline
    docblocks in PHP.

.. sidebar:: Matching PyStrings in your Step Definition

    In your step definition, there's no need to find this text and match it in
    your pattern. The text will automatically be passed as the last
    argument into the step definition method. For example:

    .. code-block:: php

        use Behat\Gherkin\Node\PyStringNode;

        // ...

        /**
         * @Given a blog post named :title with:
         */
        public function blogPost($title, PyStringNode $markdown)
        {
            $this->createPost($title, $markdown->getRaw());
        }

    PyStrings are stored in a ``PyStringNode`` instance, which you can simply
    convert to a string with ``(string) $pystring`` or ``$pystring->getRaw()``
    as in the example above.

.. note::

    Indentation of the opening ``"""`` is not important, although common practice
    is two spaces in from the enclosing step. The indentation inside the triple
    quotes, however, is significant. Each line of the string passed to the step
    definition's callback will be de-indented according to the opening ``"""``.
    Indentation beyond the column of the opening ``"""`` will therefore be
    preserved.

.. _`great post`: https://sites.google.com/site/unclebobconsultingllc/the-truth-about-bdd