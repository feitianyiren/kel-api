#!/bin/bash
set -ev

here=$(cd "$(dirname "${BASH_SOURCE}")"; pwd -P)
. $here/_common.sh

git archive --format=tar "$TRAVIS_COMMIT" | {
    docker run \
        --interactive \
        --eenv STACK=cedar-14 \
        --env BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python.git#v79 \
        --env DISABLE_COLLECTSTATIC=1 \
        $BUILDER_IMAGE -
} > $BUNDLE_FILE
