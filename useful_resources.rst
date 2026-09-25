Useful Resources & Extensions
=============================

Behat Extensions
----------------

There are a wide range of extensions already available. These include integrations with
common PHP application frameworks, browser automation, test result reporters, data fixtures
and many more.

We do not currently maintain an official list of extensions -
`most extensions can be found on GitHub`_.


Integrating Behat with PHPStorm
-------------------------------

More information on integrating Behat with PHPStorm can be found in this
`blog post`_.

.. _assertion-tools:

Assertion tools
---------------

Behat does not officially recommend an assertion library - you can use any code that
throws an Exception on failure. You can use more than one library in parallel (or
no library, for simple assertions).

Some well-known options are:

- `zenstruck/assert`_ - specifically designed for dependency-free test assertions,
  which is reflected in the information it provides when assertions fail.
- `beberlei/assert`_ - primarily designed as a fast, lightweight input validation
  library for business models and runtime code.
- `webmozarts/assert`_ - inspired by beberlei/assert and also designed for runtime
  assertions, but with more control over failure messages.

.. admonition:: Caution with PHPUnit
    :class: caution

    Behat docs used to suggest using PHPUnit's assertions. PHPUnit's author has
    explicitly stated that using PHPUnit assertions outside of PHPUnit itself
    is not supported or covered by any backwards compatibility promise.

    We **strongly recommend** that you use a different assertion tool in new
    projects.

    If you have PHPUnit assertions in an existing project, we recommend
    planning to migrate these. In the meantime, `behat/phpunit-assertions-extension`_
    provides the required bootstrapping on PHPUnit >= 11.3.0, and renders the
    details of failing assertions in your Behat output.

    Behat 3.x has partial support for older PHPUnit versions - we recommend
    installing the extension for better compatibility. Behat 4.x does not
    have any built-in PHPUnit support so you will need to add the extension
    before upgrading.


Behat cheat sheet
-----------------

An interesting `Behat and Mink cheat sheet`_ developed by `Jean-François Lépine`_

.. _`most extensions can be found on GitHub`: https://github.com/search?o=desc&q=behat+extension+in%3Aname%2Cdescription&ref=searchresults&s=stars&type=Repositories&utf8=%E2%9C%93
.. _`blog post`: http://blog.jetbrains.com/phpstorm/2014/07/using-behat-in-phpstorm/
.. _`webmozarts/assert`: https://github.com/webmozarts/assert
.. _`beberlei/assert`: https://github.com/beberlei/assert
.. _`zenstruck/assert`: https://github.com/zenstruck/assert
.. _`behat/phpunit-assertions-extension`: https://github.com/behat/PHPUnitAssertionsExtension
.. _`Behat and Mink cheat sheet`: http://blog.lepine.pro/images/2012-04-behat-cheat-sheet1.pdf
.. _`Jean-François Lépine`: http://blog.lepine.pro
