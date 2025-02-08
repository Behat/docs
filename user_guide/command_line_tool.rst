Command Line Tool
=================

This is a summary of the usage of Behat in the command line:

.. code-block:: console

    Usage:
      behat [options] [--] [<paths>]

    Arguments:
      paths
          Optional path(s) to execute. Could be:
           - a dir (features/)
           - a feature (*.feature)
           - a scenario at specific line (*.feature:10).
           - all scenarios at or after a specific line
              (*.feature:10-*).
           - all scenarios at a line within a specific range
              (*.feature:10-20).
           - a scenarios list file (*.scenarios).

    Options:
      -s, --suite=SUITE
          Only execute a specific suite.
      -f, --format=FORMAT
          How to format tests output. pretty is default.
          Available formats are:
          - pretty: Prints the feature as is.
          - progress: Prints one character per step.
          - junit: Outputs the failures in JUnit compatible
          files.
          You can use multiple formats at the same time.
          (multiple values allowed)
      -o, --out=OUT
          Write format output to a file/directory instead of
          STDOUT (output_path). You can also provide different
          outputs to multiple formats. This option is mandatory
          for the junit formatter. (multiple values allowed)
      --format-settings=FORMAT-SETTINGS
          Set formatters parameters using json object.
          Keys are parameter names, values are values. (multiple
          values allowed)
      --init
          Initialize all registered test suites.
      --lang=LANG
          Print output in particular language.
      --name=NAME
          Only execute the feature elements which match part
          of the given name or regex. (multiple values allowed)
      --tags=TAGS
          Only execute the features or scenarios with tags
          matching tag filter expression. (multiple values
          allowed)
      --role=ROLE
          Only execute the features with actor role matching
          a wildcard.
      --narrative=NARRATIVE
          Only execute the features with actor description
          matching a regex.
      --story-syntax
          Print *.feature example.
          Use --lang to see specific language.
      -d, --definitions=DEFINITIONS
          Print all available step definitions:
          - use --definitions l to just list definition
          expressions.
          - use --definitions i to show definitions with extended
          info.
          - use --definitions 'needle' to find specific
          definitions.
          Use --lang to see definitions in specific language.
      --snippets-for[=SNIPPETS-FOR]
          Specifies which context class to generate snippets for.
      --snippets-type=SNIPPETS-TYPE
          Specifies which type of snippets (turnip, regex) to
          generate.
      --append-snippets
          Appends snippets for undefined steps into main context.
      --no-snippets
          Do not print snippets for undefined steps after stats.
      --strict
          Passes only if all tests are explicitly passing.
      --print-unused-definitions
          Reports definitions that were never used.
      --order=ORDER
          Set an order in which to execute the specifications
          (this will result in slower feedback).
      --rerun
          Re-run scenarios that failed during last execution,
          or run everything if there were no failures.
      --rerun-only
          Re-run scenarios that failed during last execution,
          or exit if there were no failures.
      --stop-on-failure
          Stop processing on first failed scenario.
      --dry-run
          Invokes formatters without executing the tests and
          hooks.
      -p, --profile=PROFILE
          Specify config profile to use.
      -c, --config=CONFIG
          Specify config file to use.
      -v, --verbose[=VERBOSE]
          Increase verbosity of exceptions.
          Use -vv or --verbose=2 to display backtraces in
          addition to exceptions.
      -h, --help
          Display this help message.
      --config-reference
          Display the configuration reference.
      --debug
          Provide debugging information about current
          environment.
      -V, --version
          Display version.
      -n, --no-interaction
          Do not ask any interactive question.
      --colors
          Force ANSI color in the output. By default color
          support is guessed based on your platform and the
          output if not specified.
      --no-colors
          Force no ANSI color in the output.
      --xdebug
          Allow Xdebug to run.

.. toctree::
   :maxdepth: 2

   command_line_tool/identifying
   command_line_tool/formatting
   command_line_tool/informative_output

