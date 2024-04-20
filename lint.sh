#! /bin/bash

set -a
source config.env
set +a
poetry run black . && poetry run isort . && poetry run mypy --config-file mypy.init .
