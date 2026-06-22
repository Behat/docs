Backwards Compatibility and the Behat Public API
================================================

Behat follows Semantic Versioning. For minor or patch releases, we aim to keep things stable:

* CLI arguments and options will stay the same. We may add new ones, but existing ones will continue to work as they do
  now.
* Configuration options will not change or be removed. New options may be added, and their default values will match
  the previous behavior.
* Machine-readable output (like JSON or JUnit) will keep the same fields and data types. We might add new fields or
  change how text is formatted (like adding or removing whitespace), but the structure will remain compatible.
* Any changes to the public API (interfaces, classes, and behavior) will be backwards-compatible with the previous
  version.
* Your code (step definitions, hooks, transformations) will run the same way between versions - including
  that we will trigger hooks in the same order.
* Behat's event dispatcher will fire the same events in the same order. We might add new events in between, but
  existing ones will stay.

The only time we might break this is to fix a critical bug or a security issue that cannot be resolved any other way.

Note that from version 4.0 onwards, we do not guarantee the exact format of human-readable output (like the ``progress``
or ``pretty`` formatters). These are intended for people to read, so we may improve them over time.

What counts as Behat's "Public API"?
------------------------------------

Starting with version 3.30.0, all interfaces, classes, and methods in Behat are **internal by default**. We follow the
`phpstan backwards compatibility convention`_, which means code is only part of our public API if it is explicitly
marked with the ``@api`` tag.

* In Behat 4.0 and later, our compatibility promise only applies to code marked with ``@api``. Anything else may change
  in any release.
* In Behat 3.x, we maintain compatibility for the entire codebase. However, if you are using code that is not
  marked ``@api``, we recommend updating your code or asking us to make it public.

.. note::

    We are happy to consider making more of the Behat codebase public. If you need an ``@api`` tag added, please let
    us know! We will look at your use case and see how it affects the long-term maintenance of Behat.

    Please open an issue (or even better a Pull Request) with details on what you would like to use and why.

Classes
~~~~~~~

* Only (non-final) classes with ``@api`` in their PHPDoc can be extended.
* Objects can only be created via ``new`` if the PHPDoc of the
  public constructor is directly tagged with ``@api``. In all other cases
  (even if the class PHPDoc has ``@api``), instances of the class should
  only be created by / retrieved from Behat's service container.
* Methods can only be called if there is an ``@api`` tag in the PHPDoc
  of the method, declaring class, or declaring interface.
* Constants can only be accessed if there is an ``@api`` tag in the
  PHPDoc of the constant, declaring class, or declaring interface.

Interfaces
~~~~~~~~~~

* Interfaces with ``@api`` in their PHPDoc can be implemented and extended.
* All methods from interfaces with ``@api`` in their PHPDoc can be called.

Traits
~~~~~~

* No Behat traits can be used.


Other tips for extension authors
--------------------------------

Our compatibility promise covers changes to existing code, but we will still add new features like CLI arguments,
config options, or methods.

To avoid conflicts with future versions of Behat, we recommend following these practices:

* Do not use the ``Behat`` namespace for your own code.
* Only add configuration options within your extension's own namespace.
* While you can add new CLI commands or flags, it's safer to use configuration files or Behat's ``--profile`` feature.
  This avoids naming conflicts with future Behat versions.
* If you extend a Behat class (marked ``@api``), try to avoid adding new public methods. This protects you if Behat adds
  a method with the same name in the future.

.. _`phpstan backwards compatibility convention`: https://phpstan.org/developing-extensions/backward-compatibility-promise
