#! /bin/bash

set -a
source config.env
set +a
poetry run pytest
