#!/bin/bash
set -ev

here=$(cd "$(dirname "${BASH_SOURCE}")"; pwd -P)
. $here/_common.sh

git archive --format=tar "$TRAVIS_COMMIT" | docker run -i -e DISABLE_COLLECTSTATIC=1 -e STACK=cedar-14 -e BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python.git $BUILDER_IMAGE - > $BUNDLE_FILE
