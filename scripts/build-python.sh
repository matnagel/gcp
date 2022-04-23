#!/bin/sh
set -e

DEBIAN_FRONTEND=noninteractive apt-get -yq install tox
cd python/billing
make test
make deploy
