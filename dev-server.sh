#! /bin/bash

set -a
source config.dev.env
set +a
poetry run uvicorn src.api:app --reload