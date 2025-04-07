#!/bin/bash
set -o errexit
set -o nounset

command="${1:-build}"

if [ "$command" == 'build' ] ; then
  echo "Building docs"
  exec python -m sphinx -T -W --keep-going -b html -d _build/doctrees -D language=en . _build/html

elif [ "$command" == 'serve' ] ; then
  echo "Serving live docs on http://localhost:$SPHINX_PORT"
  # Note the --write-all option (= -a) which forces a full rather than incremental build.
  # This is because sphinx does not properly update theme and similar files on incremental builds
  # See https://github.com/sphinx-doc/sphinx-autobuild?tab=readme-ov-file#relevant-sphinx-bugs
  #
  # Also note the host 0.0.0.0 here is from inside the docker container.
  exec sphinx-autobuild --write-all --host 0.0.0.0 --port "$SPHINX_PORT" . _build/html

else
  echo "Unknown command $command"
  exit 1;
fi
