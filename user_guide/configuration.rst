Configuration
=============

.. toctree::
   :maxdepth: 2

   configuration/feature_suite_and_scenario_configuration

Custom Autoloading
------------------

Sometimes you will need to place your ``features`` folder somewhere other than the
default location (e.g. ``app/features``). All you need to do is specify the path
you want to autoload via ``behat.yml``:

.. code-block:: yaml

    # behat.yml

    default:
        autoload:
            '': %paths.base%/app/features/bootstrap

If you wish to namespace your features (for example: to be PSR-1 complaint) you will need to add the namespace to the classes and also tell behat where to load them. Here ``contexts`` is an array of classes:

.. code-block:: yaml


    # behat.yml

    default:
        autoload:
            '': %paths.base%/app/features/bootstrap
        suites:
            default:
                contexts: [My\Application\Namespace\Bootstrap\FeatureContext]

.. note::

    Using ``behat.yml`` to autoload will only allow for ``PSR-0``
    You can also use ``composer.json`` to autoload, which will also
    allow for ``PSR-4``

Formatters
----------

Default formatters can be enabled by specifying them in the profile.

.. code-block:: yaml

    # behat.yml

    default:
        formatters:
            pretty: true