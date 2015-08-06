Hooking into the Test Process
=============================

You've learned :doc:`how to write step definitions </user_guide/feature_contexts/defining_step_definitions>` and
that with :doc:`Gherkin </user_guide/gherkin_language>` you can move common steps into a
background block, making your features DRY. But what if that's not enough? What
if you want to execute some code before the whole test suite or after a
specific scenario? Hooks to the rescue:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Testwork\Hook\Scope\BeforeSuiteScope;
    use Behat\Behat\Hook\Scope\AfterScenarioScope;

    class FeatureContext implements Context
    {
        /**
         * @BeforeSuite
         */
         public static function prepare(BeforeSuiteScope $scope)
         {
             // prepare system for test suite
             // before it runs
         }

         /**
          * @AfterScenario @database
          */
         public function cleanDB(AfterScenarioScope $scope)
         {
             // clean database after scenarios,
             // tagged with @database
         }
    }

Behat Hook System
-----------------

Behat provides a number of hook points which allow us to run arbitrary
logic at various points in the Behat test cycle. Hooks are a lot like
step definitions or transformations - they are just simple methods
with special annotations inside your context classes. There is no
association between where the hook is defined and which node it is run
for, but you can use tagged or named hooks if you want more fine grained
control.

All defined hooks are run whenever the relevant action occurs. The action
tree looks something like this:

.. code-block:: text

    ├── Suite #1
    │   ├── Feature #1
    │   │   ├── Scenario #1
    │   │   │   ├── Step #1
    │   │   │   └── Step #2
    │   │   └── Scenario #2
    │   │       ├── Step #1
    │   │       └── Step #2
    │   └── Feature #2
    │       └── Scenario #1
    │           └── Step #1
    └── Suite #2
        └── Feature #1
            └── Scenario #1
                └── Step #1

This is a basic test cycle in Behat. There are many test suites, each of
which has many features, which themselves have many scenarios with many
steps. Note that when Behat actually runs, scenario outline examples are
interpreted as scenarios - meaning each outline example becomes an actual
scenario in this action tree.

.. _user-guide--feature-contexts--hooking-into-the-test-process--hooks:

Hooks
-----

Hooks allow you to execute your custom code just before or just after each
of these actions. Behat allows you to use the following hooks:

#. The ``BeforeSuite`` hook is run before any feature in the suite runs. For
   example, you could use this to set up the project you are testing. This
   hook receives an optional argument with an instance of the
   ``Behat\Testwork\Hook\Scope\BeforeSuiteScope`` class.

#. The ``AfterSuite`` hook is run after all features in the suite have run.
   This hooks is useful to dump or print some kind of statistics or tear
   down your application after testing. This hook receives an optional
   argument with an instance of the
   ``Behat\Testwork\Hook\Scope\AfterSuiteScope`` class.

#. The ``BeforeFeature`` hook is run before a feature runs. This hook receives
   an optional argument with an instance of the
   ``Behat\Behat\Hook\Scope\BeforeFeatureScope`` class.

#. The ``AfterFeature`` hook is run after Behat finishes executing a feature.
   This hook receives an optional argument with an instance of the
   ``Behat\Behat\Hook\Scope\AfterFeatureScope`` class.

#. The ``BeforeScenario`` hook is run before a specific scenario will run. This
   hook receives an optional argument with an instance of the
   ``Behat\Behat\Hook\Scope\BeforeScenarioScope`` class.

#. The ``AfterScenario`` hook is run after Behat finishes executing a scenario.
   This hook receives an optional argument with an instance of the
   ``Behat\Behat\Hook\Scope\AfterScenarioScope`` class.

#. The ``BeforeStep`` hook is run before a step runs. This hook receives an
   optional argument with an instance of the
   ``Behat\Behat\Hook\Scope\BeforeStepScope`` class.

#. The ``AfterStep`` hook is run after Behat finishes executing a step. This
   hook receives an optional argument  with an instance of the
   ``Behat\Behat\Hook\Scope\AfterStepScope`` class.

You can use any of these hooks by annotating any of your methods in your context
class:

.. code-block:: php

    /**
     * @BeforeSuite
     */
    public static function prepare($scope)
    {
        // prepare system for test suite
        // before it runs
    }

We use annotations as we did before with :doc:`definitions </user_guide/feature_contexts/defining_step_definitions>`.
Simply use the annotation of the name of the hook you want to use (e.g.
``@BeforeSuite``).

Suite Hooks
-----------
Suite hooks are run outside of the scenario context. It means that your context
class (e.g. ``FeatureContext``) is not instantiated yet and the only way Behat
can execute code in it is through the static calls. That is why suite hooks must
be defined as static methods in the context class:

.. code-block:: php

    use Behat\Testwork\Hook\Scope\BeforeSuiteScope;
    use Behat\Testwork\Hook\Scope\AfterSuiteScope;

    /** @BeforeSuite */
    public static function setup(BeforeSuiteScope $scope)
    {
    }

    /** @AfterSuite */
    public static function teardown(AfterSuiteScope $scope)
    {
    }

There are two suite hook types available:

* ``@BeforeSuite`` - executed before any feature runs.
* ``@AfterSuite`` - executed after all features have run.

Tagged Hooks
------------

Sometimes you may want a certain hook to run only for certain scenarios,
features or steps. This can be achieved by associating a ``@BeforeFeature``,
``@AfterFeature``, ``@BeforeScenario``, ``@AfterScenario``, ``@BeforeStep`` or
``@AfterStep`` hook with one or more tags. You can also use ``OR`` (``||``)
and ``AND`` (``&&``) tags:

.. code-block:: php

    /**
     * @BeforeScenario @database,@orm
     */
    public function cleanDatabase()
    {
        // clean database before
        // @database OR @orm scenarios
    }

Use the ``&&`` tag to execute a hook only when it has *all* provided tags:

.. code-block:: php

    /**
     * @BeforeScenario @database&&@fixtures
     */
    public function cleanDatabaseFixtures()
    {
        // clean database fixtures
        // before @database @fixtures
        // scenarios
    }

Scenario Hooks
--------------

Scenario hooks are triggered before or after each scenario runs. These
hooks are executed inside an initialized context instance, so not only could they
be simple context instance methods, they will also have access to
any object properties you set during your scenario:

.. code-block:: php

    use Behat\Behat\Hook\Scope\BeforeScenarioScope;
    use Behat\Behat\Hook\Scope\AfterScenarioScope;

    /** @BeforeScenario */
    public function before(BeforeScenarioScope $scope)
    {
    }

    /** @AfterScenario */
    public function after(AfterScenarioScope $scope)
    {
    }

There are two scenario hook types available:

* ``@BeforeScenario`` - executed before every scenario in each feature.
* ``@AfterScenario`` - executed after every scenario in each feature.

Now, the interesting part:

The ``@BeforeScenario`` hook executes not only
before each scenario in each feature, but before **each example row** in
the scenario outline. Yes, each scenario outline example row works almost the
same as a usual scenario.

``@AfterScenario`` functions exactly the same way, being executed both after
usual scenarios and outline examples.

Feature Hooks
-------------

Same as suite hooks, feature hooks are ran outside of the scenario context.
So same as suite hooks, your feature hooks should be defined as static methods
inside your context:

.. code-block:: php

    use Behat\Behat\Hook\Scope\BeforeFeatureScope;
    use Behat\Behat\Hook\Scope\AfterFeatureScope;

    /** @BeforeFeature */
    public static function setupFeature(BeforeFeatureScope $scope)
    {
    }

    /** @AfterFeature */
    public static function teardownFeature(AfterFeatureScope $scope)
    {
    }


There are two feature hook types available:

* ``@BeforeFeature`` - gets executed before every feature in suite.
* ``@AfterFeature`` - gets executed after every feature in suite.

Step Hooks
----------

Step hooks are triggered before or after each step runs. These hooks are
run inside an initialized context instance, so they are just plain context
instance methods in the same way as scenario hooks are:

.. code-block:: php

    use Behat\Behat\Hook\Scope\BeforeStepScope;
    use Behat\Behat\Hook\Scope\AfterStepScope;

    /** @BeforeStep */
    public function beforeStep(BeforeStepScope $scope)
    {
    }

    /** @AfterStep */
    public function after(AfterStepScope $scope)
    {
    }


There are two step hook types available:

* ``@BeforeStep`` - executed before every step in each scenario.
* ``@AfterStep`` - executed after every step in each scenario.