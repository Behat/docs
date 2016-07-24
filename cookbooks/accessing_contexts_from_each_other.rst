Accessing Contexts from each other
==================================

When splitting the definitions in multiple contexts, it might be useful to
access a context from another one. This is particularly useful when migrating
from Behat 2.x to replace subcontexts.

Behat allows to access the environment in
:doc:`hooks </user_guide/context/hooks>`,
so other contexts can be retrieved using a ``BeforeScenario`` hook:

.. code-block:: php

    use Behat\Behat\Context\Context;
    use Behat\Behat\Hook\Scope\BeforeScenarioScope;

    class FeatureContext implements Context
    {
        /** @var \Behat\MinkExtension\Context\MinkContext */
        private $minkContext;

        /** @BeforeScenario */
        public function gatherContexts(BeforeScenarioScope $scope)
        {
            $environment = $scope->getEnvironment();

            $this->minkContext = $environment->getContext('Behat\MinkExtension\Context\MinkContext');
        }
    }

.. caution::

    Circular references in context objects would prevent the PHP reference
    counting from collecting contexts at the end of each scenarios, forcing
    to wait for the garbage collector to run. This would increase the memory
    usage of your Behat run. To prevent that, it is better to avoid storing
    the environment itself in your context classes. It is also better to
    avoid creating circular references between different contexts.
