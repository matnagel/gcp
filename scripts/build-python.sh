#!/bin/sh
set -e

DEBIAN_FRONTEND=noninteractive apt-get -yq install tox zip
cd python/billing
make test
make deploy
