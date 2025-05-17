Printing paths
==============

When showing test results or failures Behat will print the path to the related files. By default
the path will be relative to the current directory. This behaviour can be modified through
configuration or on the command line:

``Print Absolute Paths``: if this is set to true, Behat will print the full absolute path instead.

``Editor URL``: if this is set, Behat will surround each path with a link that, when clicked, will open
the file in your IDE. This parameter is a template which can include placeholders that Behat will replace
at run time. The available placeholders are:

- ``{relPath}``: Relative path to the file
- ``{absPath}``: Absolute path to the file
- ``{line}}``: Line number (note that this is optional and may not be available in some cases)

The specific value that you need to use will depend on your IDE and other factors (for example, it may
need to be different if you are running your code within a Docker container). Some examples could be:

- For PhpStorm: ``phpstorm://open?file={relPath}&line={line}``
- For VS Code: ``vscode://file/{absPath}:{line}``

.. note::

    The path style can be different for the visible path and the one used in the editor URL. For example you
    might have a visible relative path and use an absolute path in the URL.

These options can be set using the ``withPathOptions()`` function of the ``Profile`` config object, for example:

.. code-block:: php

    <?php
    // behat.php

    use Behat\Config\Config;
    use Behat\Config\Profile;

    return (new Config())
        ->withProfile((new Profile('default'))
            ->withPathOptions(
                printAbsolutePaths: true,
                editorUrl: 'phpstorm://open?file={relPath}&line={line}'
            ));

They can also be set as command line options (notice that the editor URL will usually need to be quoted):

.. code-block:: bash

    behat --print-absolute-paths --editor-url="phpstorm://open?file={relPath}&line={line}"
