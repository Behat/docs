Installation
============

Before you begin, ensure that you have at least PHP 5.3.3 installed.

Method #1 - Composer (the recommended one)
------------------------------------------

The official way to install Behat is through Composer. Composer is a package
manager for PHP. Not only can it install Behat for you right now, it will be
able to easily update you to the latest version later when one comes out. If
you don't have Composer already, see
`the Composer documentation`_ for
instructions. After that, just go into your project directory (or create a
new one) and run:

.. code-block:: bash

    $ php composer.phar require --dev behat/behat=~3.0.4

Then you will be able to check installed Behat version using:

.. code-block:: bash

    $ vendor/bin/behat -V

Method #2 - PHAR (an easy one)
------------------------------

An easier way to install Behat is to grab a latest ``behat.phar`` from
`the download page`_. Make sure
that you download a ``3+`` release. After downloading it, just place it in
your project folder (or create a new one) and check the installed version using:

.. code-block:: bash

    $ php behat.phar -V

.. _`the Composer documentation`: https://getcomposer.org/download/
.. _`the download page`: https://github.com/Behat/Behat/releases