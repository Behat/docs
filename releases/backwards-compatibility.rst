Backwards Compatibility and the Behat Public API
================================================

Behat follows Semantic Versioning - so for minor or patch releases we promise that:

* CLI arguments and options will not change meaning or be removed. New arguments
  and options may be added.
* Configuration options will not change meaning or be removed. New options
  may be added - their default value will match existing behaviour.
* Fields in machine-readable output formats (e.g. JSON or JUnit) will not change
  meaning or data type or be removed. New fields may be added, and the formatting
  of text fields (for example, whitespace or line breaks within descriptions)
  may change.
* Any change to the interfaces, classes, and behaviour of the public API will
  be backwards-compatible with the previous version.
* Behat will run end-user code (step definitions, hooks, transformations, etc)
  consistently (including the sequence of hooks etc) between versions.
* Behat's event dispatcher will fire the same events, in the same sequence,
  with the same properties. New events may be added before, after or between
  existing events.

The only exception to this promise is if the existing implementation contains
a bug or security issue that cannot be fixed without a behaviour change.

Note that from 4.0 onwards we do **not guarantee** the exact format or
structure of human-readable output formats (e.g. progress or pretty).

What counts as Behat's "Public API"?
------------------------------------

Since v3.30.0, all interfaces, classes and methods within the Behat codebase
are **internal by default**. We follow the
`phpstan backwards compatibility convention`_ that code is only part of our
public API if we have explicitly tagged it as ``@api``.

* In Behat >= 4.0, the backwards compatibility promise only covers code that
  meets the rules summarised below. Anything that is not tagged ``@api`` is
  subject to change in any major, minor, or patch release.
* In Behat 3.x, we will maintain backwards compatibility for the whole
  codebase - if you are using non-``@api`` code, we recommend either
  updating your integration or requesting it be published.

.. note::

    We are happy to consider requests to add ``@api`` tags to more of the
    Behat codebase. These will be assessed based on the usecase, whether it
    is possible to achieve the same thing in a different way, and the
    potential impact on ongoing maintenance and development of Behat.

    Please open an issue (or better yet a PR) with details of what you'd
    like to be published, how you will use it, and any alternatives
    you've considered.

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


Other considerations for extension authors
------------------------------------------

Bear in mind that the backwards compatibility promise only covers removing
or changing existing code. We may still add new CLI arguments, new config
options, new classes, new methods, etc.

Therefore when writing code to extend or integrate with Behat:

* Do not place your own code in any ``Behat`` namespace.
* Do not add new configuration options outside your extension's own
  config namespace (the node passed to your extension's ``::configure``
  method).
* You *can* add new CLI commands, flags and arguments - but we recommend
  avoiding this wherever possible due to the risk of naming conflicts
  with future Behat versions or other extensions. Prefer using config
  files and e.g. Behat's ``--profile`` feature to switch between modes
  from the CLI.
* If you are extending a Behat class (with an ``@api`` tag), avoid
  adding new methods where possible. This will protect you against
  naming conflicts with methods that may be added to Behat in future.

.. _`phpstan backwards compatibility convention`: https://phpstan.org/developing-extensions/backward-compatibility-promise
