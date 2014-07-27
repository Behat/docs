Migrating from Behat 1.x to 2.0
===============================

Behat 2.0 brings completely different way to handle testing part of your
features. In 1.x we had 4 separate entities: environment, step definitions,
hooks and bootstrap scripts. In 2.0 we have only one -
`Contexts </guides/4.context>`_. That's the biggest and the coolest change
since 1.x. It made features suites much cleaner and extensible.

There were less than half-year between 1.0 and 2.0 releases? Some users already
have big feature suites and don't want to rewrite them once again. For such
users, Behat 2.0 can become fully backward compatible with 3 very small steps.

Migrating Environment
---------------------

There's no such things as environment or environment configuration in Behat2.
But :doc:`FeatureContext </guides/4.context>` can successfully emulate
environment objects from Behat 1.x. Let's say, we have next ``env.php``
configuration:

.. code-block:: php

    <?php features/support/env.php

    $world->someInitialVar = 'initial-val';
    $world->closureFunc = function() {
        // do something
    };

The easiest way to migrate is to move this code into
``FeatureContext`` class:

.. code-block:: php

    <?php

    use Behat\Behat\Context\ClosuredContextInterface,
        Behat\Behat\Context\BehatContext,
        Behat\Behat\Exception\PendingException;
    use Behat\Gherkin\Node\PyStringNode,
        Behat\Gherkin\Node\TableNode;

    class FeatureContext extends BehatContext
    {
        public $someInitialVar = 'initial-val';

        public function closureFunc()
        {
            // do something
        }
    }

As you might see, your ``someInitialVar`` become an instance variable and
``closureFunc()`` just an instance method. You should move all your variables
and methods carefully, changing all ``$world`` to ``$this`` in closure methods.

It might be very hard and annoying work, especially on large projects. So, as
you might expect, you have another option:

.. code-block:: php

    <?php

    use Behat\Behat\Context\ClosuredContextInterface,
        Behat\Behat\Context\BehatContext,
        Behat\Behat\Exception\PendingException;
    use Behat\Gherkin\Node\PyStringNode,
        Behat\Gherkin\Node\TableNode;

    class FeatureContext extends BehatContext
    {
        public $parameters = array();

        public function __construct(array $parameters)
        {
            $this->parameters = $parameters;

            if (file_exists($env = __DIR__.'/../support/env.php')) {
                $world = $this;
                require_once($env);
            }
        }

        public function __call($name, array $args) {
            if (isset($this->$name) && is_callable($this->$name)) {
                return call_user_func_array($this->$name, $args);
            } else {
                $trace = debug_backtrace();
                trigger_error(
                    'Call to undefined method ' . get_class($this) . '::' . $name .
                    ' in ' . $trace[0]['file'] .
                    ' on line ' . $trace[0]['line'],
                    E_USER_ERROR
                );
            }
        }
    }

With this context, you'll be able to use your old ``env.php`` totally untouched.
That's it. Full BC with 1.x environment.

Migrating Bootstrap Scripts
---------------------------

Now, what about ``bootstrap.php``? Same story. You either move all your code
into ``features/bootstrap/FeatureContext.php`` file right before class:

.. code-block:: php

    <?php

    ...

    // require and load something here

    class FeatureContext extends BehatContext
    ...

or you can leave ``bootstrap.php`` untouched and just tell ``FeatureContext.php``
to load it by itself:

.. code-block:: php

    <?php

    ...

    if (file_exists($boot = __DIR__.'/../support/bootstrap.php')) {
        require_once($boot);
    }

    class FeatureContext extends BehatContext
    ...

That's it.

Migrating Step Definitions and Hooks
------------------------------------

That was a hard part. Yep, you've heard me right. Closured step definitions
and hooks support is much more easier to achieve, thanks to bundled with Behat2
closured loader.

The only thing, you need to do is to implement this interface with your ``FeatureContext``:

.. code-block:: php

    <?php

    namespace Behat\Behat\Context;

    interface ClosuredContextInterface extends ContextInterface
    {
        function getStepDefinitionResources();
        function getHookDefinitionResources();
    }


There's only two methods in this interface:

* ``getStepDefinitionResources()`` should return array of ``*.php`` paths, that
  will be used as step definition resources.

* ``getHookDefinitionResources()`` should return array of ``*.php`` paths, that
  will be used as hook definition resources.

For example, put next code in your ``FeatureContext``:

.. code-block:: php

    # features/bootstrap/FeatureContext.php
    <?php

    use Behat\Behat\Context\ClosuredContextInterface,
        Behat\Behat\Context\BehatContext;

    /**
     * Features context.
     */
    class FeatureContext extends BehatContext implements ClosuredContextInterface
    {
        public function getStepDefinitionResources()
        {
            return array(__DIR__ . '/../steps/basic_steps.php');
        }

        public function getHookDefinitionResources()
        {
            return array(__DIR__ . '/../support/hooks.php');
        }
    }

Now, Behat will try to load all :doc:`step definitions </guides/2.definitions>`
from out the ``features/steps/basic_steps.php`` file and
:doc:`hooks </guides/3.hooks>` from out the ``features/support/hooks.php``.

That's quite simple. But what if you have more than one definition file?
Adding all this file into array by hands can become tedious. But you always can
use ``glob()``:

.. code-block:: php

    # features/bootstrap/FeatureContext.php
    <?php

    use Behat\Behat\Context\ClosuredContextInterface,
        Behat\Behat\Context\BehatContext;

    /**
     * Features context.
     */
    class FeatureContext extends BehatContext implements ClosuredContextInterface
    {
        public function getStepDefinitionResources()
        {
            return glob(__DIR__.'/../steps/*.php');
        }

        public function getHookDefinitionResources()
        {
            return array(__DIR__ . '/../support/hooks.php');
        }
    }

Yep. We will load all ``features/steps/*.php`` files automatically. Same as this
were done in Behat 1.x.

Fully BC Context
----------------

Taking all previously said into account, fully backward-compatible context will
look like this:

.. code-block:: php

    <?php

    use Behat\Behat\Context\ClosuredContextInterface,
        Behat\Behat\Context\BehatContext,
        Behat\Behat\Exception\PendingException;
    use Behat\Gherkin\Node\PyStringNode,
        Behat\Gherkin\Node\TableNode;

    if (file_exists(__DIR__ . '/../support/bootstrap.php')) {
        require_once __DIR__ . '/../support/bootstrap.php';
    }

    class FeatureContext extends BehatContext implements ClosuredContextInterface
    {
        public $parameters = array();

        public function __construct(array $parameters) {
            $this->parameters = $parameters;

            if (file_exists(__DIR__ . '/../support/env.php')) {
                $world = $this;
                require(__DIR__ . '/../support/env.php');
            }
        }

        public function getStepDefinitionResources() {
            if (file_exists(__DIR__ . '/../steps')) {
                return glob(__DIR__.'/../steps/*.php');
            }
            return array();
        }

        public function getHookDefinitionResources() {
            if (file_exists(__DIR__ . '/../support/hooks.php')) {
                return array(__DIR__ . '/../support/hooks.php');
            }
            return array();
        }

        public function __call($name, array $args) {
            if (isset($this->$name) && is_callable($this->$name)) {
                return call_user_func_array($this->$name, $args);
            } else {
                $trace = debug_backtrace();
                trigger_error(
                    'Call to undefined method ' . get_class($this) . '::' . $name .
                    ' in ' . $trace[0]['file'] .
                    ' on line ' . $trace[0]['line'],
                    E_USER_ERROR
                );
            }
        }
    }

You can just copy'n'paste this code into your ``features/bootstrap/FeatureContext.php``
and Behat2 will magically start to work with your 1.x feature suite.
