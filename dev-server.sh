#! /bin/bash

set -a
source config.env
set +a
poetry run uvicorn src.api:app --reload