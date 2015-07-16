Initializing a new Behat Project
================================

The easiest way to start using Behat in your project is to call ``behat``
with the ``--init`` option inside your project directory:

.. code-block:: bash

    $ vendor/bin/behat --init

After you run this command, Behat will set up a ``features`` directory
inside your project:

The newly created ``features/bootstrap/FeatureContext.php`` will have
an initial context class to get you started:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\SnippetAcceptingContext;
    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements SnippetAcceptingContext
    {
        /**
         * Initializes context.
         */
        public function __construct()
        {
        }
    }

All
:doc:`step definitions</user_guide/feature_contexts/defining_step_definitions>`
and :ref:`user-guide--feature-contexts--hooking-into-the-test-process--hooks`
necessary for testing your project against your features will be represented as
methods inside this class.

.. _user-guide--initializing-a-new-behat-project--suite-initialisation:

Suite Initialisation
--------------------

Suites are a core part of Behat. Any feature of Behat knows about
them and can give you a hand with them. For example, if you defined
your suites in ``behat.yml`` before running ``--init``, it will actually
create the folders and suites you configured, instead of the default ones.