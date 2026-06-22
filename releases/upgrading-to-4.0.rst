Upgrading to Behat 4.0
======================

We want to make upgrading to Behat 4.0 as smooth as possible. While there are some breaking changes, we've tried to
keep them to a minimum.

If you are an end-user (meaning you use Behat to run tests but haven't written custom extensions), most of these changes
won't affect you. In many cases, you can use automated tools to handle the upgrade for you. Follow this guide to get
started.

Upgrading for users
--------------------

For most projects, these are the main changes:

* **PHP Configuration:** We now use PHP for configuration. YAML files are no longer supported. Behat will look for
  ``behat.php`` or ``behat.dist.php`` in your current directory.
* **PHP Attributes:** We've replaced PHPDoc annotations (like ``@Given`` or ``@BeforeScenario``) with native PHP
  Attributes.
* **Cleanup:** All previously deprecated features and code have been removed.
* **New Parser Mode:** We now default to a newer parser compatibility mode
  (:doc:`GHERKIN_32 </user_guide/gherkin/parser_mode>`).

Step-by-step preparation
~~~~~~~~~~~~~~~~~~~~~~~~~

**Before** you switch to Behat 4.0, we recommend taking these steps:

1. **Update Behat 3:** Make sure you are using the latest version of Behat 3.x.
2. **Convert Config:** If you use YAML, run ``vendor/bin/behat --convert-config`` to `convert it to PHP`_. Review the
   results to make sure everything looks correct.
3. **Check File Location:** If your config file is in a ``config/`` folder, move it to your project root or use the
   ``--config`` flag when running Behat.
4. **Update Extensions:** Make sure any extensions you use are referenced by their full class name (e.g.
   ``Behat\MinkExtension\ServiceContainer\MinkExtension::class`` not ``Behat\MinkExtension```). The conversion tool
   usually handles this.
5. **Convert Annotations:** Use `Rector`_ with the ``->withAttributeSets(behat: true)`` rule to automatically change
   `Behat annotations`_ into PHP Attributes.
6. **Check Deprecations:** Run your tests with ``--fail-on-deprecations`` and fix any warnings that appear.
7. **Test the New Parser:** Enable the :doc:`GHERKIN_32 parser mode </user_guide/gherkin/parser_mode>` and see if your
   tests still run correctly. If you have issues, you can fix your feature files or use
   ``GherkinCompatibilityMode::LEGACY`` in your config. This mode will be removed in future.

Ready to upgrade?
~~~~~~~~~~~~~~~~~

Once you've completed the steps above, update your ``composer.json`` to start using Behat 4.0!

.. caution::
   While we are in the alpha phase, we recommend using:
   ``{"require": {"behat/behat": "4.0.0-alpha1@alpha"}}``.

.. note::
   Don't forget to update your third-party extensions to versions that support Behat 4.0. If you find one that hasn't
   been updated yet, consider helping out by submitting a Pull Request! The community's help makes the transition faster
   for everyone.


Upgrading for extension authors
-------------------------------

It's possible to support both Behat 3.x and 4.x at the same time (for example, by using
``{"require": {"behat/behat": "^3.x || ^4.x"}}``).

If your project uses Behat to test itself, first follow the "Upgrading for users" steps above.

Here are the key changes for all extension authors:

* **Strict Types:** All interfaces and classes now use strict types for parameters, properties, and return values. As a
  minimum, you will need to add return types to any methods that implement Behat interfaces or extend Behat classes.
  `Rector`_ can automate this for you with the ``AddReturnTypeBasedOnParentClassMethodRector`` (included in the
  ``typeDeclarations`` set).
* **Public API:** We are now stricter about what is considered public API. This helps us maintain a solid
  :doc:`backwards compatibility promise </releases/backwards-compatibility>`. If your extension needs to use code that
  isn't marked public yet, please let us know.
* **Full Class Names:** Users can no longer use "short names" for extensions (like ``Behat\MinkExtension``). They must
  now use the fully-qualified class name of your ``Extension`` class. Please update your documentation to reflect this.
* **Deprecations:** If your extension needs to report deprecations, we recommend using
  ``Behat\Testwork\Deprecation\DeprecationCollector::trigger()`` (available since 3.30.0) instead of ``trigger_error``.
   This ensures they are correctly handled by Behat's deprecation flags regardless of the user's runtime environment.
* **Event Changes:** The ``ScenarioLikeTested`` base event class has been removed. ``ScenarioTested`` and
  ``BackgroundTested`` are now separate. This may affect you if you maintain a formatter extension.

There are several other changes that might affect a minority of extension authors. See the full
`CHANGELOG`_ for details.

Planned changes before the final 4.0.0 release
----------------------------------------------

We plan to make two more significant changes before the final 4.0.0 release:

* **Parameter Matching:** We are reviewing how steps behave when the number of function parameters doesn't match the
  step definition. This will likely trigger a deprecation or a failure. You can follow the progress in `#1691`_.
* **PHPUnit Assertions:** Support for rendering PHPUnit assertion failures will move to a standalone extension. While
  tests will still pass or fail, the output will be less detailed without the extension. We no longer recommend using
  PHPUnit for assertions within Behat steps, as the PHPUnit project has confirmed this is not supported. See
  `#1746`_ for details.

We may make additional changes based on feedback from the community as more people begin to upgrade.

.. _`convert it to PHP`: https://docs.behat.org/en/v3.x/user_guide/configuration/yaml_configuration.html#converting-your-configuration
.. _`Rector`: https://getrector.com/documentation
.. _`Behat annotations`: https://docs.behat.org/en/v3.x/user_guide/annotations.html#existing-code
.. _`AddReturnTypeBasedOnParentClassMethodRector`: https://getrector.com/rule-detail/add-return-type-declaration-based-on-parent-class-method-rector
.. _`CHANGELOG`: https://github.com/Behat/Behat/blob/4.x/CHANGELOG.md
.. _`#1691`: https://github.com/Behat/Behat/issues/1691
.. _`#1746`: https://github.com/Behat/Behat/issues/1746
