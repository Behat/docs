Integrating Symfony2 with Behat
===============================

Symfony2 is a `Web Application Framework <http://symfony.com/>`_ that can be easily integrated and used seamlessly with Behat 3.
As a prerequisite for this cookbook you need to have working Symfony2 application.

In this cookbook we will cover:

#. Installing Behat dependency with Composer.

#. Initialising Behat suite.

#. Installing and enabling Symfony2 extension.

#. Accessing application services in contexts.

#. Using Symfony2 test client as a Mink driver.

Installing Behat in your Symfony2 project
-----------------------------------------

Recommended way of managing Behat dependency in your project is to use `Composer <https://getcomposer.org/)>`_.
Assuming that you already have ``composer.json`` file in your project you only need to add one new entry to it and install.
It can be done automatically for you with this command:

.. code-block:: bash

    $ php composer.phar require --dev behat/behat

.. note::

    Note that we have used ``--dev`` switch for Composer.
    It means that Behat will be installed as as ``require-dev`` dependency in your project, and will not be present in production.
    For further information please check `Composer documentation <https://getcomposer.org/doc/04-schema.md#require-dev>`_.

Initialising Behat
------------------

After execution of this command you should see information about files initialised in your project,
and you should be able to write your first scenario.
In order to verify Behat initialisation you can just run following command:

.. code-block:: bash

    $ bin/behat

.. tip::

    If you don't feel familiar with Behat enough please read :doc:`/quick_intro_pt1` first.

Installing and enabling Symfony2 extension
------------------------------------------

Great, you have a Behat suite working in your project, now it's time to install `Symfony2Extension <https://github.com/Behat/Symfony2Extension>`_.
To do this you need to add another dependency, but in the same way we did it a while ago:

.. code-block:: bash

    $ php composer.phar require --dev behat/symfony2-extension

Now it's time to enable extension in your ``behat.yml`` file.
If it doesn't exist just create such file in your project root and fill it with following content:

.. code-block:: yaml

    default:
      extensions:
        Behat\Symfony2Extension: ~

If this file already exists just change its contents accordingly.
From that point you should be able to run Behat and Symfony2 extension will be loaded and ready to work with.

Accessing application services in contexts
------------------------------------------

The extension we have just installed detects the default Symfony configuration and allows
to use your application services in context classes. To make a service available in a context you need
to change your ``behat.yml`` configuration and tell the extension which services to inject:

.. code-block:: yaml

    default:
      suites:
        default:
            contexts:
                - FeatureContext:
                    session:   '@session'
      extensions:
        Behat\Symfony2Extension: ~

This configuration will try to to match the ``$session`` dependency of your ``FeatureContext`` constructor by injecting the ``session`` service into the context.
Be careful because if such a service does not exist or its name does not match, it will not work and you will end up with a Behat exception.

Using KernelDriver with your Behat suite
----------------------------------------

Symfony2 has a build-in Test Client, which can help you with web acceptance testing, why not make use of it?
Especially because Behat has a `Mink Extension <http://mink.behat.org>`_ that makes those kind of testing even easier.

The advantage of using KernelDriver instead of standard Mink driver is that you don't need to run web server in order to access a page.
Also you can even use `Symfony Profiler <http://symfony.com/doc/current/cookbook/testing/profiling.html>`_ and inspect your application directly!.
You can read more about test client in `Symfony Documentation <http://symfony.com/doc/current/book/testing.html#your-first-functional-test>`_.

If you don't have Mink and MinkExtension yet, you can install those two with:

.. code-block:: bash

    $ php composer.phar require --dev behat/mink
    $ php composer.phar require --dev behat/mink-extension

In order to install BrowserKit Driver you need to execute following command:

.. code-block:: bash

    $ php composer.phar require --dev behat/mink-browserkit-driver

Now you are only one step from being ready to make full use of Symfony2 extension in your project.
You need to enable extension in your ``behat.yml`` file as follows:

.. code-block:: yaml

    default:
      extensions:
        Behat\Symfony2Extension: ~
        Behat\MinkExtension:
          sessions:
            default:
              symfony2: ~

Et voilà! Now you are ready to drive your Symfony2 app development with Behat3!
