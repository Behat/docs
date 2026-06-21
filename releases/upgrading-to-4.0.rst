Upgrading to Behat 4.0
======================

We have tried to make it as easy as possible to upgrade to Behat 4.0, but it does
contain some breaking changes.

If you are an end-user (you use Behat to run your specifications, but you haven't
extended / integrated with the Behat internals), then many of these will not affect
you. We also expect that you will be able to resolve the majority of these with
automated tools - follow this guide to find out more.

Upgrading for end-users
-----------------------

For end-user projects, the major changes are:

* We no longer support YAML configuration - and we only automatically detect
  config from ``behat.php`` or ``behat.dist.php`` in the directory where you
  run Behat.
* We no longer support PHPDoc annotations to mark up step definitions, hooks and
  argument transformations.
* All deprecated features and code have been removed.
* We now default to the :doc:`GHERKIN_32 parser compatibility mode </user_guide/gherkin/parser_mode>`.

Preparing to upgrade
~~~~~~~~~~~~~~~~~~~~

**Before** you attempt to update to Behat 4.0, you should make all of these changes:

1. Ensure you are running the latest Behat 3.x
2. If you have YAML configuration, run ``vendor/bin/behat --convert-config`` to
   `convert it to the new PHP config`_. Review the output carefully - the tool will handle most
   common configurations but is not guaranteed to cater for all unusual or complex cases.
3. If your Behat config file is in a ``config/`` subdirectory, either move it to the directory
   where you run Behat, or add the ``--config {PATH TO FILE}`` argument to any Behat runs.
4. If you use any extensions, check that these are enabled using the fully-qualified class name
   of the ``Extension`` class. The ``--convert-config`` tool will usually do this for you.
5. Run `Rector`_ with the ``->withAttributeSets(behat: true)`` rule to convert any
   `Behat annotations`_ into PHP Attributes. If your project isn't already using Rector, you
   can install it temporarily and just run that rule.
6. Run your full Behat suite(s) with the ``--fail-on-deprecations`` option and fix any failures.
7. Configure Behat to use the :doc:`GHERKIN_32 parser compatibility mode </user_guide/gherkin/parser_mode>`
   and check if this affects your project. If this causes issues, you can either fix your feature
   files or update your Behat configuration to force the ``GherkinCompatibilityMode::LEGACY``.

Upgrading
~~~~~~~~~

If you have followed the steps above, you should be ready to update your composer.json and
start using Behat 4.0!

.. caution::
   We expect there will be a small number of breaking changes between 4.0.0-alpha1 and
   4.0.0. We recommend ``{"require": {"behat/behat": "4.0.0-alpha1@alpha"}}`` for now.
   See below for more details.

.. note::
   If you use any third-party Behat extensions, you will need to update these to a version
   that supports Behat 4.0. If you find an extension that hasn't yet been updated, please
   consider submitting a PR. The more the Behat community contributes to updating the
   ecosystem, the quicker we will all get there :)


Upgrading for extension authors
-------------------------------

It should be possible to support Behat 3.x and 4.x simultaneously (e.g.
``{"require": {"behat/behat": "^3.x || ^4.x"}}``).

If your project uses Behat directly (e.g. to "dog-food" your extension / run your own features)
you will first need to follow the steps above for upgrading end-user projects.

The major changes for all extension authors are:

* All interfaces and classes now have strict parameter, property & return types. You will
  need to add return types to all methods that implement Behat interfaces or extend Behat classes.
  ``Rector`` can do this for you with the ``AddReturnTypeBasedOnParentClassMethodRector``.
  This is included by default if you enable Rector's ``typeDeclarations`` set.
* We are now much stricter about what counts as the public API (and will therefore be covered
  by the :doc:`backwards compatibility promise </releases/backwards-compatibility>` in future).
  If your extension needs to use Behat code that we haven't marked as public, please let us know.
* We no longer support users referencing an extension by a "short name" (e.g. ``Behat\MinkExtension``).
  Users must always give the fully-qualified name of your ``Extension`` class. Please update your
  documentation.
* If your extension needs to report deprecations, we recommend calling
  ``Behat\Testwork\Deprecation\DeprecationCollector::trigger()`` (available since 3.30.0) instead
  of the native ``trigger_error``. This will guarantee it is handled by the ``--print-deprecations``
  / ``--fail-on-deprecations`` options in all cases.
* The ``ScenarioLikeTested`` base event class no longer exists. ``ScenarioTested`` and
  ``BackgroundTested`` are now separate event families. This is particularly likely to affect
  formatter extensions.

There are several other changes that might affect a minority of extension authors. See the full
`CHANGELOG`_ for details.


Planned changes between 4.0.0-alpha1 and 4.0.0
----------------------------------------------

There are two significant changes that we plan to make before 4.0.0:

* We will review the behaviour of steps where the number of function parameters does not match
  the number of parameters in the step definition text. As a minimum, this will trigger a
  deprecation - it may trigger a failure. See `#1691`_.
* Support for rendering details of a PHPUnit assertion failure will move out of Behat core
  into a standalone extension. Without the extension, tests will still pass/fail as expected
  but the failure output will be less useful. See `#1746`_. This is because PHPUnit assertions
  are not designed to be used outside PHPUnit and we no longer recommend using PHPUnit for
  assertions within Behat steps.

We may make more changes before 4.0, depending on feedback from extension authors as they start
to upgrade.

.. _`convert it to the new PHP config`: https://docs.behat.org/en/3.x/user_guide/configuration/yaml_configuration.html#converting-your-configuration
.. _`Rector`: https://getrector.com/documentation
.. _`Behat annotations`: https://docs.behat.org/en/v3.x/user_guide/annotations.html#existing-code
.. _`AddReturnTypeBasedOnParentClassMethodRector`: https://getrector.com/rule-detail/add-return-type-declaration-based-on-parent-class-method-rector
.. _`CHANGELOG`: https://github.com/Behat/Behat/blob/4.x/CHANGELOG.md
.. _`#1691`: https://github.com/Behat/Behat/issues/1691
.. _`#1746`: https://github.com/Behat/Behat/issues/1746
