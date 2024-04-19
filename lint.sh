#! /bin/bash

set -a
source config.dev.env
set +a
poetry run black . && poetry run isort . && poetry run mypy --config-file mypy.init .
