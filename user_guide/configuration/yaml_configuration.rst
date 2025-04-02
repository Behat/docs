Yaml configuration
==================

Currently the preferred way to define the configuration for your Behat project
is by using one or more files with PHP configuration.

But historically this configuration could also be expressed in files in the Yaml
format. This possibility is still available for now, and you can use it instead
of PHP configuration in your projects - however it will likely be deprecated and
removed in the future.

Here is an example of how some configuration could look using a Yaml file:

.. code-block:: yaml

    imports:
        - imported.yaml

    default:
        formatters:
            progress: ~
            junit: false
        suites:
            my_suite:
                contexts:
                    - MyContext
                paths:
                    - "one.feature"
                filters:
                    tags: "@run"
        extensions:
            MyCustomExtension: ~

Converting your configuration
-----------------------------

If your project uses the legacy Yaml format for your configuration, you can easily
convert them to the PHP format by using the built in config converter.

To use it, just run:

.. code-block:: bash

    vendor/bin/behat --convert-config

This will load the default config file loaded by your project and convert it from the
Yaml format to the PHP format. It will also convert any config files that are imported
by this main file. It will then remove the old Yaml files.

We recommend carefully reviewing the generated config, particularly if you are using extensions,
custom formatters, or have complex configuration files.

If you want to convert any other config file which is not your default config file (for
example a config file used in the CI environment), just load it with the ``-c``
(or ``--config``) option like this:

.. code-block:: bash

    vendor/bin/behat --convert-config -c ci-behat.yml

This will load the ``ci-behat.yml`` config file and convert it to the PHP format.

.. note::

    Behat needs to be able to load this config file before converting it, so it must be
    a valid Behat config file.
