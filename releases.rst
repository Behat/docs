Releases & version support
==========================

Behat follows `Semantic Versioning`_ - therefore we will only make breaking changes to the Public API in a major
release. Note that a significant portion of Behat's codebase is **not considered part of the Public API** - you
can read more in :doc:`the Backward Compatibility documentation </releases/backwards-compatibility>`.

Supported versions
------------------

======= ========== ========== ============ =======================================================================
Major   Released   Bugfix EOL Security EOL
======= ========== ========== ============ =======================================================================
`v3.x`_ April 2014 See below  See below    `Changelog <https://github.com/Behat/Behat/blob/3.x/CHANGELOG.md>`__
`v4.x`_ tbc 2025/6 See below  See below    `Changelog <https://github.com/Behat/Behat/blob/4.x/CHANGELOG.md>`__
======= ========== ========== ============ =======================================================================

As a minimum, a major version series will receive:

* Bugfixes for 12 months after the release of the next major.
* Security fixes for 24 months after the release of the next major.

Each time a new major version is released, the Behat maintainers will set End-of-Life dates for the previous version
series. This will be based on the scale of the breaking changes, the complexity of supporting the older version, and the
likely effort required for users and third-party extensions to upgrade.

Bugfixes will usually only be applied to the most recent minor of each supported major version, unless they are
particularly severe or have security implications. This will impact
:ref:`support for End-of-Life PHP & Symfony versions<Support for PHP and dependency versions>`.

Release timescales
------------------

There is no fixed schedule for releasing new major versions - but we will try to keep them to a frequency that is
manageable for users.

Minor versions
~~~~~~~~~~~~~~

Minor & patch versions will be released whenever there is something to release. These releases do not come with any
specific support timescale, and we expect that users will upgrade to the next minor when it becomes available.

Please bear in mind that this is free software, maintained by volunteers as a gift to users, and the license
specifically explains that it is provided without warranty of any kind.


Support for PHP and dependency versions
---------------------------------------

Behat only supports current versions of PHP and third-party dependency packages (e.g. Symfony components).

By "current", we mean:

* PHP versions that are listed as receiving active support or security fixes
  on the `official php.net version support page`_.
* Symfony versions that are listed as maintained or receiving security fixes on the `official Symfony releases page`_.

Note that Symfony 8 introduces breaking changes to interfaces that Behat cannot support without ourselves making
breaking changes. Therefore, Symfony 8 will only be supported from Behat 4.0 onwards.

Once a PHP or Symfony version reaches End of Life we will remove it from our composer.json and CI flows.

.. note::
   When we drop support for a PHP / dependency version we will highlight this in the CHANGELOG, but we will treat
   it as a minor release. Composer will automatically protect users from upgrading to a version that does not support
   their environment. Users running Behat as a ``.phar`` should review the release notes before downloading
   a new version.

We will not ship bugfix releases for unsupported PHP / dependency versions, unless:

* It fixes a security vulnerability within the security support period for a Behat major version.
* An external contributor wishes to take on the work of backporting, including any changes required
  to get a green build in CI.

End-of-Life versions
--------------------

These behat series are no longer maintained and will not receive any further releases. We strongly recommend that users
upgrade to a supported version as soon as possible.

======= ========== ============ ============ =====================================================================
Major   Released   Bugfix EOL   Security EOL
======= ========== ============ ============ =====================================================================
`v2.x`_ July 2011  June 2015    June 2015    `Changelog <https://github.com/Behat/Behat/blob/2.5/CHANGES.md>`__
======= ========== ============ ============ =====================================================================

Additional Releases documentation
---------------------------------

.. toctree::
   :maxdepth: 1

   releases/backwards-compatibility

.. _`Semantic Versioning`: http://semver.org/
.. _`official php.net version support page`: https://www.php.net/supported-versions.php
.. _`official Symfony releases page`: https://symfony.com/releases
.. _`v2.x`: https://github.com/Behat/Behat/releases?q=v2
.. _`v3.x`: https://github.com/Behat/Behat/releases?q=v3
.. _`v4.x`: https://github.com/Behat/Behat/releases?q=v4
