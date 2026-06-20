Useful Resources & Extensions
=============================

Behat Extensions
----------------

There are a wide range of extensions already available. These include integrations with
common PHP application frameworks, browser automation, test result reporters, data fixtures
and many more.

We do not currently maintain an official list of extensions -
`most extensions can be found on GitHub`_.


Integrating Behat with PHPStorm
-------------------------------

More information on integrating Behat with PHPStorm can be found in this
`blog post`_.

.. _assertion-tools:

Assertion tools
---------------

A proper assertion tool is a library whose assertions throw exceptions on failure.

For example a list of the most known:

- https://github.com/webmozarts/assert
- https://github.com/beberlei/assert
- https://github.com/zenstruck/assert

.. admonition:: Caution with PHPUnit
    :class: caution

    If you are familiar with PHPUnit, you can use its assertion library

    .. code-block:: bash

        $ php composer.phar require --dev phpunit/phpunit

    and then by simply using assertions in your steps:

    .. code-block:: php

        \PHPUnit\Framework\Assert::assertCount(
            intval($count),
            $this->basket
        );

    **WARNING: using PHPUnit for assertions no longer works with PHP 11.3.0 and later out-of-the-box**.

    This is due to a change in how PHPUnit's internal components are initialized. The recommended workaround
    to use the PHPUnit assertions is to bootstrap PHPUnit during Behat execution from a ``BeforeSuite`` hook:

    .. code-block:: php

        use Behat\Hook\BeforeSuite;

        class FeatureContext {

            #[BeforeSuite]
            public static function initPhpunit() {
                (new \PHPUnit\TextUI\Configuration\Builder())->build([]);
            }
        }

    If you have multiple suites, you may want to use a static variable in the hook to ensure the initialization only
    runs once.

    Learn more at https://github.com/Behat/Behat/issues/1618.


Behat cheat sheet
-----------------

An interesting `Behat and Mink cheat sheet`_ developed by `Jean-François Lépine`_

.. _`most extensions can be found on GitHub`: https://github.com/search?o=desc&q=behat+extension+in%3Aname%2Cdescription&ref=searchresults&s=stars&type=Repositories&utf8=%E2%9C%93
.. _`blog post`: http://blog.jetbrains.com/phpstorm/2014/07/using-behat-in-phpstorm/
.. _`Behat and Mink cheat sheet`: http://blog.lepine.pro/images/2012-04-behat-cheat-sheet1.pdf
.. _`Jean-François Lépine`: http://blog.lepine.pro
