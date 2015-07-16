Feature Contexts
================

We've already used this strange ``FeatureContext`` class as a home for our
:doc:`step definitions </user_guide/feature_contexts/defining_step_definitions>`
and :ref:`user-guide--feature-contexts--hooking-into-the-test-process--hooks`,
but we haven't done much to explain what it actually is.

Context classes are a keystone of testing environment in Behat. The context
class is a simple POPO (Plain Old PHP Object) that tells Behat how to test
your features. If ``*.feature`` files are all about describing *how* your
application behaves, then the context class is all about how to test it.

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        public function __construct($parameter)
        {
            // instantiate context
        }

        /** @BeforeFeature */
        public static function prepareForTheFeature()
        {
            // clean database or do other preparation stuff
        }

        /** @Given we have some context */
        public function prepareContext()
        {
            // do something
        }

        /** @When event occurs */
        public function doSomeAction()
        {
            // do something
        }

        /** @Then something should be done */
        public function checkOutcomes()
        {
            // do something
        }
    }

A simple mnemonic for context classes is "testing features *in a context*".
Feature descriptions tend to be very high level. It means there's not much
technical detail exposed in them, so the way you will test those
features pretty much depends on the context you test them in. That's what
context classes are.

.. tip::

  This class can be easily created by running
  :doc:`Behat command line tool</user_guide/command_line_tool>` with the
  ``--init`` command from your project's directory. Behat is able to support
  you when you are creating a new project. Learn more about
  ":doc:`/user_guide/initializing_a_new_behat_project`".


.. toctree::
   :maxdepth: 2

   feature_contexts/hooking_into_the_test_process
   feature_contexts/defining_step_definitions


Context Class Requirements
--------------------------

In order to be used by Behat, your context class should follow these rules:

#. The context class should implement the ``Behat\Behat\Context\Context`` interface.

#. The context class should be called ``FeatureContext``. It's a simple convention
   inside the Behat infrastructure. ``FeatureContext`` is the name of the
   context class for the default suite. This can easily be changed through
   suite configuration inside ``behat.yml``.

#. The context class should be discoverable and loadable by Behat. That means you
   should somehow tell Behat about your class file. Behat comes with a PSR-0
   autoloader out of the box and the default autoloading directory is
   ``features/bootstrap``. That's why the default ``FeatureContext`` is loaded so
   easily by Behat. You can place your own classes under ``features/bootstrap``
   by following the PSR-0 convention or you can even define your own custom
   autoloading folder via ``behat.yml``.

.. note::

    ``Behat\Behat\Context\SnippetAcceptingContext`` and
    ``Behat\Behat\Context\CustomSnippetAcceptingContext`` are special
    versions of the ``Behat\Behat\Context\Context`` interface that tell
    Behat this context expects snippets to be generated for it.

.. tip::

   The :doc:`Behat command line tool</user_guide/command_line_tool>`
   has an ``--init`` option that will initialize a new Behat project in your
   directory. Learn more about
   :doc:`/user_guide/initializing_a_new_behat_project`.

Contexts Lifetime
-----------------

Your context class is initialized before each scenario is run, and every scenario
has its very own context instance. This means 2 things:

#. Every scenario is isolated from each other scenario's context. You can do
   almost anything inside your scenario context instance without the fear of
   affecting other scenarios - every scenario gets its own context instance.

#. Every step in a single scenario is executed inside a common context
   instance. This means you can set ``private`` instance variables inside
   your ``@Given`` steps and you'll be able to read their new values inside
   your ``@When`` and ``@Then`` steps.

Multiple Contexts
-----------------

At some point, it could become very hard to maintain all your
:doc:`step definitions </user_guide/feature_contexts/defining_step_definitions>`
and :ref:`user-guide--feature-contexts--hooking-into-the-test-process--hooks`
inside a single class. You could use class inheritance and split definitions
into multiple classes, but doing so could cause your code to become more
difficult to follow and use.

In light of these issues, Behat provides a more flexible way of helping make
your code more structured by allowing you to use multiple contexts in a single test
suite.

In order to customise the list of contexts your test suite requires, you need
to fine-tune the suite configuration inside ``behat.yml``:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - FeatureContext
                    - SecondContext
                    - ThirdContext

The first ``default`` in this configuration is a name of the profile. We
will discuss profiles a little bit later. Under
the specific profile, we have a special ``suites`` section, which
configures suites inside profile. We will talk about test suites in more
detail in the :doc:`next chapter </user_guide/configuration>`, for now just keep in mind
that a suite is a way to tell Behat where to find your features and
how to test them. The interesting part for us now is the ``contexts``
section - this is an array of context class names. Behat will use the classes
specified there as your feature contexts. This means that every time
Behat sees a scenario in your test suite, it will:

#. Get list of all context classes from this ``contexts`` option.

#. Will try to initialize all these context classes into objects.

#. Will search for :doc:`step definitions </user_guide/feature_contexts/defining_step_definitions>` and
   :ref:`user-guide--feature-contexts--hooking-into-the-test-process--hooks` in all of them.

.. note::

    Do not forget that each of these context classes should follow all
    context class requirements. Specifically - they all should implement
    ``Behat\Behat\Context\Context`` interface and be autoloadable by
    Behat.

Basically, all contexts under ``contexts`` section of your ``behat.yml``
are the same for Behat. It will find and use the methods in them the same way
it does in the default ``FeatureContext``. And if you're happy with a single
context class, but you don't like the name ``FeatureContext``, here's
how you change it:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext

This configuration will tell Behat to look for ``MyAwesomeContext``
instead of the default ``FeatureContext``.

.. note::

    Unlike profiles, Behat will not inherit any configuration of your
    ``default`` suite. The name ``default`` is only used for demonstration
    purpose in this guide. If you have multiple suites that all should use the
    same context, you will have to define that specific context for every
    specific suite:

    .. code-block:: yaml

        # behat.yml

        default:
            suites:
                default:
                    contexts:
                        - MyAwesomeContext
                        - MyWickedContext
                suite_a:
                    contexts:
                        - MyAwesomeContext
                        - MyWickedContext
                suite_b:
                    contexts:
                        - MyAwesomeContext

    This configuration will tell Behat to look for ``MyAwesomeContext`` and
    ``MyWickedContext`` when testing ``suite_a`` and ``MyAwesomeContext`` when
    testing ``suite_b``. In this example, ``suite_b`` will not be able to call
    steps that are defined in the ``MyWickedContext``. As you can see, even if
    you are using the name ``default`` as the name of the suite, Behat will not
    inherit any configuration from this suite.

Context Parameters
------------------

Context classes can be very flexible depending on how far you want
to go in making them dynamic. Most of us will want to make our contexts
environment-independent; where should we put temporary files, which URLs
will be used to access the application? These are
context configuration options highly dependent on the environment you
will test your features in.

We already said that context classes are just plain old PHP classes.
How would you incorporate environment-dependent parameters into your
PHP classes? Use *constructor arguments*:

.. code-block:: php

    // features/bootstrap/MyAwesomeContext.php

    use Behat\Behat\Context\Context;

    class MyAwesomeContext implements Context
    {
        public function __construct($baseUrl, $tempPath)
        {
            $this->baseUrl = $baseUrl;
            $this->tempPath = $tempPath;
        }
    }

As a matter of fact, Behat gives you ability to do just that. You can
specify arguments required to instantiate your context classes through
same ``contexts`` setting inside your ``behat.yml``:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext:
                        - http://localhost:8080
                        - /var/tmp

.. note::

    Note an indentation for parameters. It is significant:

    .. code-block:: yaml

        contexts:
            - MyAwesomeContext:
                - http://localhost:8080
                - /var/tmp

    Aligned four spaces from the context class itself.

Arguments would be passed to the ``MyAwesomeContext`` constructor in
the order they were specified here. If you are not happy with the idea
of keeping an order of arguments in your head, you can use argument
names instead:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext:
                        baseUrl: http://localhost:8080
                        tempPath: /var/tmp

As a matter of fact, if you do, the order in which you specify these
arguments becomes irrelevant:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext:
                        tempPath: /var/tmp
                        baseUrl: http://localhost:8080

Taking this a step further, if your context constructor arguments are
optional:

.. code-block:: php

    public function __construct($baseUrl = 'http://localhost', $tempPath = '/var/tmp')
    {
        $this->baseUrl = $baseUrl;
        $this->tempPath = $tempPath;
    }

You then can specify only the parameter that you actually need to change:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext:
                        tempPath: /var/tmp

In this case, the default values would be used for other parameters.

Context Traits
--------------

PHP 5.4 have brought an interesting feature to the language - traits.
Traits are a mechanism for code reuse in single inheritance languages
like PHP. Traits are implemented as a compile-time copy-paste in PHP.
That means if you put some step definitions or hooks inside a trait:

.. code-block:: php

    // features/bootstrap/ProductsDictionary.php

    trait ProductsDictionary
    {
        /**
         * @Given there is a(n) :arg1, which costs £:arg2
         */
        public function thereIsAWhichCostsPs($arg1, $arg2)
        {
            throw new PendingException();
        }
    }

And then use it in your context:

.. code-block:: php

    // features/bootstrap/MyAwesomeContext.php

    use Behat\Behat\Context\Context;

    class MyAwesomeContext implements Context
    {
        use ProductsDictionary;
    }

It will just work as you expect it to.

