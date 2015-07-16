Feature, Suite and Scenario Configuration
=========================================

We already talked about configuring multiple contexts for a single test
suite in a :doc:`previous chapter </user_guide/feature_contexts>`. Now it is
time to talk about test suites themselves. A test suite represents a group of
concrete features together with the information on how to test them.

With suites you can configure Behat to test different kinds of features
using different kinds of contexts and doing so in one run. Test suites are
really powerful and ``behat.yml`` makes them that much more powerful:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            core_features:
                paths:    [ %paths.base%/features/core ]
                contexts: [ CoreDomainContext ]
            user_features:
                paths:    [ %paths.base%/features/web ]
                filters:  { role: user }
                contexts: [ UserContext ]
            admin_features:
                paths:    [ %paths.base%/features/web ]
                filters:  { role: admin }
                contexts: [ AdminContext ]

Suite Paths
-----------

One of the most obvious settings of the suites is the ``paths``
configuration:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            core_features:
                paths:
                    - %paths.base%/features
                    - %paths.base%/test/features
                    - %paths.base%/vendor/.../features

As you might imagine, this option tells Behat where to search for test features.
You could, for example, tell Behat to look into the
``features/web`` folder for features and test them with ``WebContext``:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            web_features:
                paths:    [ %paths.base%/features/web ]
                contexts: [ WebContext ]

You then might want to also describe some API-specific features in
``features/api`` and test them with an API-specific ``ApiContext``. Easy:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            web_features:
                paths:    [ %paths.base%/features/web ]
                contexts: [ WebContext ]
            api_features:
                paths:    [ %paths.base%/features/api ]
                contexts: [ ApiContext ]

This will cause Behat to:

#. Find all features inside ``features/web`` and test them using your
   ``WebContext``.

#. Find all features inside ``features/api`` and test them using your
   ``ApiContext``.

.. note::

    ``%paths.base%`` is a special variable in ``behat.yml`` that refers
    to the folder in which ``behat.yml`` is stored.

Path-based suites are an easy way to test highly-modular applications
where features are delivered by highly decoupled components. With suites
you can test all of them together.

Suite Filters
-------------

In addition to being able to run features from different directories,
we can run scenarios from the same directory, but filtered by specific
criteria. The Gherkin parser comes bundled with a set of cool filters
such as *tags* and *name* filters. You can use these filters to run
features with specific tag (or name) in specific contexts:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            web_features:
                paths:    [ %paths.base%/features ]
                contexts: [ WebContext ]
                filters:
                    tags: @web
            api_features:
                paths:    [ %paths.base%/features ]
                contexts: [ ApiContext ]
                filters:
                    tags: @api

This configuration will tell Behat to run features and scenarios
tagged as ``@web`` in ``WebContext`` and features and scenarios
tagged as ``@api`` in ``ApiContext``. Even if they all are stored
in the same folder. How cool is that? But it gets even better,
because Gherkin 4+ (used in Behat 3+) added a very special *role*
filter. That means, you can now have nice actor-based suites:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            user_features:
                paths:    [ %paths.base%/features ]
                contexts: [ UserContext ]
                filters:
                    role: user
            admin_features:
                paths:    [ %paths.base%/features ]
                contexts: [ AdminContext ]
                filters:
                    role: admin

A Role filter takes a look into the feature description block:

.. code-block:: gherkin

    Feature: Registering users
      In order to help more people use our system
      As an admin
      I need to be able to register more users

It looks for a ``As a ...`` or ``As an ...`` pattern and guesses its
actor from it. It then filters features that do not have the expected
actor from the set. In the case of our example, it basically means that
features described from the perspective of the *user* actor will
be tested in ``UserContext`` and features described from the
perspective of the *admin* actor will be tested in ``AdminContext``.
Even if they are in the same folder.

While it is possible to specify filters as part of suite configuration,
sometimes you will want to exclude certain scenarios across the suite, with the
option to override the filters at the command line.

This is achieved by specifying the filter in the gherkin configuration:

.. code-block:: yaml

    # behat.yml

    default:
        gherkin:
          filters:
            tags: ~@wip

In this instance, scenarios tagged as @wip will be ignored unless the CLI
command is run with a custom filter, e.g.:

.. code-block:: bash

    vendor/bin/behat --tags=wip

.. tip::

   More details on identifying tests can be found in the chapter
   :doc:`/user_guide/command_line_tool/identifying_tests`.

Extensions
----------

Extensions can be configured like this:

.. code-block:: yaml

    # behat.yml

    default:
    	extensions:
            Behat\MinkExtension:
                base_url: http://www.example.com
            	selenium2: ~

Suite Contexts
--------------

Being able to specify a set of features with a set of contexts for
these features inside the suite has a very interesting side-effect.
You can specify the same features in two different suites being tested
against different contexts *or* the same contexts configured differently.
This basically means that you can use the same subset of features to
develop different layers of your application with Behat:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            domain_features:
                paths:    [ %paths.base%/features ]
                contexts: [ DomainContext ]
            web_features:
                paths:    [ %paths.base%/features ]
                contexts: [ WebContext ]
                filters:
                    tags: @web

In this case, Behat will first run all the features from the ``features/``
folder in ``DomainContext`` and then only those tagged with ``@web`` in
 ``WebContext``.

.. tip::

   It might be worth reading how to :ref:`execute a specific
   suite<user-guide--command-line-tool--identifying-tests--by-suite>` or
   :ref:`initializing a new
   suite<user-guide--initializing-a-new-behat-project--suite-initialisation>`