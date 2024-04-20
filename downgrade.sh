#! /bin/bash

set -a
source config.env
set +a
poetry run alembic downgrade base
