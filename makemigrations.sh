#! /bin/bash

set -a
source config.dev.env
set +a
poetry run alembic revision --autogenerate -m "$1"
