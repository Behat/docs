Defining Step Definitions
=========================

:doc:`Gherkin language</user_guide/gherkin_language>` provides a way to describe your
application behavior in business understandable language. But how do you test
that the described behavior is actually implemented? Or that the application
satisfies your business expectations as described in the feature scenarios?
Behat provides a way to map your scenario steps (actions) 1-to-1 with actual
PHP code called step definitions:

.. code-block:: php

    /**
     * @When I do something with :argument
     */
    public function iDoSomethingWith($argument)
    {
        // do something with $argument
    }

.. note::

   Step definitions are just normal PHP methods. They are instance methods in
   a special class called :doc:`FeatureContext</user_guide/feature_contexts>`.

Creating Your First Step Definition
-----------------------------------

The main goal for a step definition is to be executed when Behat sees its matching
step in executed scenario. However, just because a method exists within ``FeatureContext``
doesn't mean Behat can find it. Behat needs a way to check that a concrete class
method is suitable for a concrete step in a scenario. Behat matches
``FeatureContext`` methods to step definitions using pattern matching.

When Behat runs, it compares lines of Gherkin steps from each scenario to the
patterns bound to each method in your ``FeatureContext``. If the line of Gherkin
satisfies a bound pattern, its corresponding step definition is executed. It's
that simple!

Behat uses php-doc annotations to bind patterns to ``FeatureContext`` methods:

.. code-block:: php

    /**
     * @When I do something with :methodArgument
     */
    public function someMethod($methodArgument) {}

Let's take a closer look at this code:

#. ``@When`` is a definition keyword. There are 3 supported keywords in
   annotations: ``@Given``/``@When``/``@Then``. These three definition keywords
   are actually equivalent, but all three are available so that your step
   definition remains readable.

#. The text after the keyword is the step text pattern (e.g.
   ``I do something with :methodArgument``).

#. All token values of the pattern (e.g. ``:methodArgument``) will be captured
   and passed to the method argument with the same name (``$methodArgument``).

.. note::

    Notice the comment block starts with ``/**``, and not the usual ``/*``.
    This is important for Behat to be able to parse such comments as annotations!

As you have probably noticed, this pattern is quite general and its corresponding
method will be called for steps that contain ``... I do something with ...``,
including:

.. code-block:: gherkin

    Given I do something with "string1"
    When I do something with 'some other string'
    Then I do something with 25

The only real difference between those steps in the eyes of Behat is the
captured token text. This text will be passed to the step's corresponding
method as an argument value. In the example above,
``FeatureContext::someMethod()`` will be called three times, each time with
a different argument:

#. ``$context->someMethod($methodArgument = 'string1');``.

#. ``$context->someMethod($methodArgument = 'some other string');``.

#. ``$context->someMethod($methodArgument = '25');``.

.. note::

    A pattern can't automatically determine the datatype of its matches, so
    all method arguments coming from step definitions are passed as strings.
    Even if your pattern matches "500", which could be considered an integer,
    '500' will be passed as a string argument to the step definition's method.

    This is not a feature or limitation of Behat, but rather the inherent way
    string matching works. It is your responsibility to cast string arguments
    to integers, floats or booleans where applicable given the code you are
    testing.

    Casting arguments to specific types can be accomplished using
    `step argument transformations`_.

.. note::

    Behat does not differentiate between step keywords when matching patterns
    to methods. So a step defined with ``@When`` could also be matched to
    ``@Given ...``, ``@Then ...``, ``@And ...``, ``@But ...``, etc.

Your step definitions can also define multiple arguments to pass to its matching
``FeatureContext`` method:

.. code-block:: php

    /**
     * @When I do something with :stringArgument and with :numberArgument
     */
    public function someMethod($stringArgument, $numberArgument) {}

You can also specify alternative words and optional parts of words, like this:

.. code-block:: php

    /**
     * @When there is/are :count monster(s)
     */
    public function thereAreMonsters($count) {}

If you need to come up with a much more complicated matching algorithm, you can
always use good old regular expressions:

.. code-block:: php

    /**
     * @When /^there (?:is|are) (\d+) monsters?$/i
     */
    public function thereAreMonsters($count) {}

Definition Snippets
-------------------

You now know how to write step definitions by hand, but writing all these
method stubs, annotations and patterns by hand is tedious. Behat makes
this routine task much easier and fun by generating definition snippets for
you! Let's pretend that you have this feature:

.. code-block:: gherkin

    Feature:
      Scenario:
        Given some step with "string" argument
        And number step with 23

If your context class implements ``Behat\Behat\Context\SnippetAcceptingContext``
interface and you test a feature with missing steps in Behat:

.. code-block:: bash

    $ vendor/bin/behat features/example.feature

Behat will provide auto-generated snippets for your context class.

It not only generates the proper definition annotation type (``@Given``), but
also a proper pattern with tokens capturing (``:arg1``, ``:arg2``), method
name (``someStepWithArgument()``, ``numberStepWith()``) and arguments (
``$arg1``, ``$arg2``), all based just on the text of the step. Isn't that cool?

The only thing left for you to do is to copy these method snippets into your
``FeatureContext`` class and provide a useful body for them. Or even better,
run behat with ``--append-snippets`` option:

.. code-block:: bash

    $ vendor/bin/behat features/example.feature --dry-run --append-snippets

``--append-snippets`` tells Behat to automatically add snippets inside your
context class.

.. note::

    Implementing the ``SnippetAcceptingContext`` interface tells Behat that
    your context is expecting snippets to be generated inside it. Behat will
    generate simple pattern snippets for you, but if regular expressions
    are your thing, Behat can generate them instead if you implement
    ``Behat\Behat\Context\CustomSnippetAcceptingContext`` interface instead
    and add ``getAcceptedSnippetType()`` method returning string ``"regex"``:

    .. code-block:: php

        public static function getAcceptedSnippetType()
        {
            return 'regex';
        }

Step Execution Result Types
---------------------------

Now you know how to map actual code to PHP code that will be executed. But
how can you tell what exactly "failed" or "passed" when executing a step?
And how does Behat actually check that a step executed properly?

For that, we have step execution types. Behat differentiates between seven
types of step execution results: "`Successful Steps`_", "`Undefined Steps`_",
"`Pending Steps`_", "`Failed Steps`_", "`Skipped Steps`_", "`Ambiguous Steps`_"
and "`Redundant Step Definitions`_".

Let's use our previously introduced feature for all the following examples:

.. code-block:: gherkin

    # features/example.feature
    Feature:
      Scenario:
        Given some step with "string" argument
        And number step with 23

Successful Steps
~~~~~~~~~~~~~~~~

When Behat finds a matching step definition it will execute it. If the
definition method does **not** throw any ``Exception``, the step is marked
as successful (green). What you return from a definition method has no
effect on the passing or failing status of the definition itself.

Let's pretend our context class contains the code below:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /** @Given some step with :argument1 argument */
        public function someStepWithArgument($argument1)
        {
        }

        /** @Given number step with :argument1 */
        public function numberStepWith($argument1)
        {
        }
    }

When you run your feature, you'll see all steps passed and are marked as
green. That's simply because no exceptions were thrown during their
execution.

.. note::

    Passed steps are always marked as **green** if colors are supported by
    your console.

.. tip::

    Enable the "posix" PHP extension in order to see colorful Behat output.
    Depending on your Linux, Mac OS or other Unix system it might be part
    of the default PHP installation or a separate ``php5-posix`` package.

Undefined Steps
~~~~~~~~~~~~~~~

When Behat cannot find a matching definition, the step is marked as
**undefined**, and all subsequent steps in the scenarios are **skipped**.

Let's pretend we have an empty context class:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
    }

When you run your feature, you'll get 2 undefined steps that are marked
yellow.

.. note::

    Undefined steps are always marked as **yellow** if colors are supported by
    your console.

.. note::

    All steps following an undefined step are not executed, as the
    behavior following it is unpredictable. These steps are marked as
    **skipped** (cyan).

.. tip::

    If you use the ``--strict`` option with Behat, undefined steps will cause
    Behat to exit with ``1`` code.

Pending Steps
~~~~~~~~~~~~~

When a definition method throws a
``Behat\Behat\Tester\Exception\PendingException`` exception, the step is
marked as **pending**, reminding you that you have work to do.

Let's pretend your ``FeatureContext`` looks like this:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Behat\Tester\Exception\PendingException;

    class FeatureContext implements Context
    {
        /** @Given some step with :argument1 argument */
        public function someStepWithArgument($argument1)
        {
            throw new PendingException('Do some string work');
        }

        /** @Given number step with :argument1 */
        public function numberStepWith($argument1)
        {
            throw new PendingException('Do some number work');
        }
    }

When you run your feature, you'll get 1 pending step that is marked yellow and
one step following it that is marked cyan.

.. note::

    Pending steps are always marked as **yellow** if colors are supported by
    your console, because they are logically similar to **undefined** steps.

.. note::

    All steps following a pending step are not executed, as the
    behavior following it is unpredictable. These steps are marked as
    **skipped**.

.. tip::

    If you use ``--strict`` option with Behat, pending steps will cause Behat
    to exit with ``1`` code.

Failed Steps
~~~~~~~~~~~~

When a definition method throws any ``Exception`` (except ``PendingException``)
during execution, the step is marked as **failed**. Again, what you return from a
definition does not affect the passing or failing of the step. Returning ``null``
or ``false`` will not cause a step to fail.

Let's pretend, that your ``FeatureContext`` has following code:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /** @Given some step with :argument1 argument */
        public function someStepWithArgument($argument1)
        {
            throw new Exception('some exception');
        }

        /** @Given number step with :argument1 */
        public function numberStepWith($argument1)
        {
        }
    }

When you run your feature, you'll get 1 failing step that is marked red and
it will be followed by 1 skipped step that is marked cyan.

.. note::

    Failed steps are always marked as **red** if colors are supported by
    your console.

.. note::

    All steps within a scenario following a failed step are not executed, as the
    behavior following it is unpredictable. These steps are marked as
    **skipped**.

.. tip::

    If Behat finds a failed step during suite execution, it will exit with
    ``1`` code.

.. tip::

    Behat doesn't come with its own assertion tool, but you can use any proper assertion
    tool out there. Proper assertion tool is a library, which assertions throw
    exceptions on fail. For example, if you're familiar with PHPUnit, you can use
    its assertions in Behat by installing it via composer:

    .. code-block:: bash

        $ php composer.phar require --dev phpunit/phpunit='~4.1.0'

    and then by simply using assertions in your steps:

    .. code-block:: php

        PHPUnit_Framework_Assert::assertCount(intval($count), $this->basket);

.. tip::

    You can get exception stack trace with ``-vv`` option provided to Behat:

    .. code-block:: bash

        $ vendor/bin/behat features/example.feature -vv

Skipped Steps
~~~~~~~~~~~~~

Steps that follow **undefined**, **pending** or **failed** steps are never
executed, even if there is a matching definition. These steps are marked
**skipped**:

.. note::

    Skipped steps are always marked as **cyan** if colors are supported by
    your console.

Ambiguous Steps
~~~~~~~~~~~~~~~

When Behat finds two or more definitions that match a single step, this step is
marked as **ambiguous**.

Consider your ``FeatureContext`` has following code:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /** @Given /^.* step with .*$/ */
        public function someStepWithArgument()
        {
        }

        /** @Given /^number step with (\d+)$/ */
        public function numberStepWith($argument1)
        {
        }
    }

Executing Behat with this feature context will result in a ``Ambiguous``
exception being thrown.

Behat will not make a decision about which definition to execute. That's your
job! But as you can see, Behat will provide useful information to help you
eliminate such problems.

Redundant Step Definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~

Behat will not let you define a step expression's corresponding pattern more
than once. For example, look at the two ``@Given`` patterns defined in this
feature context:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /** @Given /^number step with (\d+)$/ */
        public function workWithNumber($number1)
        {
        }

        /** @Given /^number step with (\d+)$/ */
        public function workDifferentlyWithNumber($number1)
        {
        }
    }

Executing Behat with this feature context will result in a ``Redundant``
exception being thrown.

Step Argument Transformations
-----------------------------

Step argument transformations allow you to abstract common operations performed
on step definition arguments into reusable methods. In addition, these methods
can be used to transform a normal string argument that was going to be used
as an argument to a step definition method, into a more specific data type
or an object.

Each transformation method must return a new value. This value then replaces
the original string value that was going to be used as an argument to a step
definition method.

Transformation methods are defined using the same annotation style as step
definition methods, but instead use the ``@Transform`` keyword, followed by
a matching pattern.

As a basic example, you can automatically cast all numeric arguments to
integers with the following context class code:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /**
         * @Transform /^(\d+)$/
         */
        public function castStringToNumber($string)
        {
            return intval($string);
        }

        /**
         * @Then a user :name, should have :count followers
         */
        public function assertUserHasFollowers($name, $count)
        {
            if ('integer' !== gettype($count)) {
                throw new Exception('Integer expected');
            }
        }
    }

.. note::

    In the same way as with step definitions, you can use both simple patterns and
    regular expressions.

Let's go a step further and create a transformation method that takes an
incoming string argument and returns a specific object. In the following
example, our transformation method will be passed a username, and the method
will create and return a new ``User`` object:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /**
         * @Transform :user
         */
        public function castUsernameToUser($user)
        {
            return new User($user);
        }

        /**
         * @Then a :user, should have :count followers
         */
        public function assertUserHasFollowers(User $user, $count)
        {
            if ('integer' !== gettype($count)) {
                throw new Exception('Integer expected');
            }
        }
    }

Table Transformation
~~~~~~~~~~~~~~~~~~~~

Let's pretend we have written the following feature:

.. code-block:: gherkin

    # features/table.feature
    Feature: Users

      Scenario: Creating Users
        Given the following users:
          | name          | followers |
          | everzet       | 147       |
          | avalanche123  | 142       |
          | kriswallsmith | 274       |
          | fabpot        | 962       |

And our ``FeatureContext`` class looks like this:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements Context
    {
        /**
         * @Given the following users:
         */
        public function pushUsers(TableNode $usersTable)
        {
            $users = array();
            foreach ($usersTable as $userHash) {
                $user = new User();
                $user->setUsername($userHash['name']);
                $user->setFollowersCount($userHash['followers']);
                $users[] = $user;
            }

            // do something with $users
        }
    }

A table like this may be needed in a step testing the creation of the
``User`` objects themselves, and later used again to validate other parts of
our codebase that depend on multiple ``User`` objects that already exist.
In both cases, our transformation method can take our table of usernames and
follower counts and build dummy ``User`` objects. By using a transformation
method we have eliminated the need to duplicate the code that creates our
``User`` objects, and can instead rely on the transformation method each time
this functionality is needed.

Transformations can also be used with tables. A table transformation is matched
via a comma-delimited list of the column headers prefixed with ``table:``:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements Context
    {
        /**
         * @Transform table:name,followers
         */
        public function castUsersTable(TableNode $usersTable)
        {
            $users = array();
            foreach ($usersTable->getHash() as $userHash) {
                $user = new User();
                $user->setUsername($userHash['name']);
                $user->setFollowersCount($userHash['followers']);
                $users[] = $user;
            }

            return $users;
        }

        /**
         * @Given the following users:
         */
        public function pushUsers(array $users)
        {
            // do something with $users
        }

        /**
         * @Then I expect the following users:
         */
        public function assertUsers(array $users)
        {
            // do something with $users
        }
    }

.. note::

    Transformations are powerful and it is important to take care how you
    implement them. A mistake can often introduce strange and unexpected
    behavior. Also, they are inherently hard to debug because of their
    highly dynamic nature.


.. tip::
   Behat provides a :ref:`command line
   option<user-guide--comand-line-tool--informative-output--print-definitions>`
   that allows you to easily browse definitions in order to reuse them or adapt
   them.
