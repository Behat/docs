Configuration
=============

Behat has a very powerful configuration system based on ``PHP`` configuration files and
profiles.

.. toctree::
   :maxdepth: 2

   configuration/suites.rst
   configuration/printing_paths.rst

``behat.php``
-------------

All configuration happens inside a single PHP configuration file. By default, Behat loads
the configuration from your current working directory from the first file matching:

#. ``behat.php``
#. ``behat.dist.php``

You can also tell Behat where your config file is with the ``--config`` option:

.. code-block:: bash

    $ behat --config custom-config.php

.. note::

   From Behat 4.0, we no longer support the old YAML config format. You can
   automatically convert this to PHP before you upgrade - see
   :doc:`the 4.0 upgrade guide </releases/upgrading-to-4.0>`.

All configuration parameters in that file are defined under a profile. A profile is just
a custom name you can use to quickly switch testing configuration by using the
``--profile`` option when executing your feature suite.

The default profile is always ``default``. All other profiles inherit
parameters from the ``default`` profile. If you only need one profile, define
all of your parameters under the ``default`` profile:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Profile;

    return new Config()
        ->withProfile(
            new Profile('default')
            //...
        )
    ;

Overriding ``default`` params
-----------------------------

Each profile is an extension of the ``default`` profile. This means you can
define a new profile that overrides configuration parameters defined in the
``default`` profile.

Let's assume we have a ``default`` profile as such:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Filter\TagFilter;
    use Behat\Config\Profile;
    use Behat\Config\Suite;

    $defaultSuite = new Suite('default')
        ->withFilter(new TagFilter('@runthisonlyondefault'))
    ;

    return new Config()
        ->withProfile(
            new Profile('default')
                ->withSuite($defaultSuite)
        )
    ;

Now we want a profile that changes the tag which is to be run in the default
suite. We can add the profile and just override:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Filter\TagFilter;
    use Behat\Config\Profile;
    use Behat\Config\Suite;

    $defaultSuite = new Suite('default')
        ->withFilter(new TagFilter('@runthisonlyondefault'))
    ;

    $profile1DefaultSuite = new Suite('default')
        ->withFilter(new TagFilter('@runthisonlyonprofile1'))
    ;

    return new Config()
        ->withProfile(
            new Profile('default')
                ->withSuite($defaultSuite)
        )
        ->withProfile(
            new Profile('profile1')
                ->withSuite($profile1DefaultSuite)
        )
    ;

Or maybe we want to unset the tag filter for a profile:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Filter\TagFilter;
    use Behat\Config\Profile;
    use Behat\Config\Suite;

    $defaultSuite = new Suite('default')
        ->withFilter(new TagFilter('@runthisonlyondefault'))
    ;

    $profile1DefaultSuite = new Suite('default', ['filters' => null]);

    return new Config()
        ->withProfile(
            new Profile('default')
                ->withSuite($defaultSuite)
        )
        ->withProfile(
            new Profile('profile1')
                ->withSuite($profile1DefaultSuite)
        )
    ;

Importing Config
----------------

The ``import`` methods can be used to merge multiple configuration files in to
one loaded config in Behat, using the following syntax:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;

    return new Config()
        ->import([
            'config/base.behat.php',
            'config/ci.behat.php',
        ])
    ;

All files from the ``import`` method will be loaded by Behat and merged, in
the listed order, into your ``behat.php`` config. This is especially useful
when you want to tweak configuration slightly between local development and
on Continuous Integration environments by using partial configuration files.

This allows configuration files listed in the ``import`` method to override
configuration values for previously listed files.

Global profile configuration
----------------------------

You can set some global configuration in your profile configuration:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;

    return new Config()
        ->withProfile(
            new Profile('default', [
                'testers' => [
                    // these are the default values
                    'stop_on_failure' => false,
                    'strict' => false,
                ],
            ])
        )
    ;

Combining the fact that you can override the default profile, you can change the configuration per profile:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;

    return new Config()
        ->withProfile(
            new Profile('default', [
                'testers' => [
                    'stop_on_failure' => true,
                    'strict' => false,
                ],
            ])
        )
        ->withProfile(
            new Profile('ci', [
                'testers' => [
                    'stop_on_failure' => false,
                    'strict' => true,
                ],
            ])
        )
    ;

This way, with the default profile behat will stop on failure and won't be
 strict, but will not stop and will be strict if the CI profile is selected.

You can force ``--stop-on-failure`` and ``--strict`` via CLI options to override
configuration values.

Environment Variable - BEHAT_PARAMS
-----------------------------------

If you want to set up configurable Behat settings, use the ``BEHAT_PARAMS``
environment variable:

.. code-block:: bash

    export BEHAT_PARAMS='{"extensions" : {"Behat\\MinkExtension" : {"base_url" : "https://www.example.com/"}}}'

You can set any value for any option that is available in a ``behat.php`` file.
Just provide options in *JSON* format. Behat will use those options as defaults.
You can always override them with the settings in the project ``behat.php``
file (it has higher priority).

.. tip::

   You can convert the PHP configuration to JSON using the ``toArray`` method.

    .. code-block:: php

        <?php
        // behat.php
        use Behat\Config\Config;
        use Behat\Config\Filter\TagFilter;
        use Behat\Config\Profile;

        $config = new Config()
            ->withProfile(
                new Profile('default')
                    ->withFilter(new TagFilter('~@wip'))
            )
        ;

        var_dump(json_encode($config->toArray()));

    .. code-block:: json

        {"default":{"gherkin":{"filters":{"tags":"~@wip"}}}}

.. tip::

    In order to specify a parameter in an environment variable, the value
    *must not* exist in your ``behat.php``

.. tip::

    NOTE: In Behat 2.x this variable was in *URL* format.  It has been changed
    to use *JSON* format.

Global Filters
--------------

While it is possible to specify filters as part of suite configuration,
sometimes you will want to exclude certain scenarios across the suite,
with the option to override the filters at the command line.

This is achieved by specifying the filter in the ``gherkin`` configuration:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Filter\TagFilter;
    use Behat\Config\Profile;

    return new Config()
        ->withProfile(
            new Profile('default')
                ->withFilter(new TagFilter('~@wip'))
        )
    ;

In this instance, scenarios tagged as ``@wip`` will be ignored unless the CLI command is run with a custom filter, e.g.:

.. code-block:: bash

    vendor/bin/behat --tags=wip

Custom Autoloading
------------------

Sometimes you will need to place your ``features`` folder somewhere other than the
default location (e.g. ``app/features``). All you need to do is specify the path
you want to autoload via ``behat.php``:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Profile;

    return new Config()
        ->withProfile(
            new Profile('default', [
                'autoload' => [
                    '' => '%paths.base%/app/features/bootstrap',
                ],
            ])
        )
    ;

If you wish to namespace your features (for example: to be PSR-1 compliant)
you will need to add the namespace to the classes and also tell behat where
to load them. Here ``contexts`` is an array of classes:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Profile;
    use Behat\Config\Suite;

    $defaultProfile = new Profile('default', [
        'autoload' => [
            '' => '%paths.base%/app/features/bootstrap',
        ],
    ]);

    $defaultProfile->withSuite(
        new Suite('default')
            ->withContexts('My\Application\Namespace\Bootstrap\FeatureContext')
    );

    return new Config()
        ->withProfile($defaultProfile)
    ;

Using ``behat.php`` to autoload will only allow for ``PSR-0``.
You can also use ``composer.json`` to autoload, which will also allow for ``PSR-4``:

.. code-block:: json

    {
      "autoload-dev": {
        "psr-4": {
          "My\\Application\\Namespace\\Bootstrap\\": "app/features/bootstrap"
        }
      }
    }

If you add this to your ``composer.json`` file, then you won't need to specify autoloading in
your ``behat.php`` file:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Profile;
    use Behat\Config\Suite;

    $defaultProfile = new Profile('default')
        ->withSuite(
            new Suite('default')
                ->withContexts('My\Application\Namespace\Bootstrap\FeatureContext')
        )
    ;

    return new Config()
        ->withProfile($defaultProfile)
    ;

Formatters
----------

Default formatters can be enabled by specifying them in the profile.

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Profile;
    use Behat\Config\Formatter\PrettyFormatter;

    return new Config()
        ->withProfile(
            new Profile('default')
                ->withFormatter(
                    new PrettyFormatter()
                )
        )
    ;

Extensions
----------

Extensions can be configured like this:

.. code-block:: php

    <?php
    // behat.php
    use Behat\Config\Config;
    use Behat\Config\Profile;
    use Behat\Config\Formatter\PrettyFormatter;
    use Behat\MinkExtension\ServiceContainer\MinkExtension;

    return new Config()
        ->withProfile(
            new Profile('default')
                >withExtension(
                    new Extension(MinkExtension::class, [
                        'base_url' => 'http://www.example.com',
                        'selenium2' => null,
                    ])
                )
        )
    ;
