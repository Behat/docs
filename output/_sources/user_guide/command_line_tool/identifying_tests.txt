Identifying Tests
=================

.. _user-guide--command-line-tool--identifying-tests--by-suite:

By Suite
--------

By default, when you run Behat it will execute all registered suites
one-by-one. If you want to run a single suite instead, use the ``--suite``
option:

.. code-block:: bash

    $ vendor/bin/behat --suite=web_features
