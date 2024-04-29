# Shopery

## Setting up the project

Copy the config template:

``cp config.template.env config.env``

And fill the variables with your configuration

Then, assuming that you have Docker and docker-compose installed:

``make up``

``make migrate``

Only during the initial setup:

``make bootstrap`` (will create S3 buckets)

## Other commands

``make down`` – stop and remove the project containers

``make build`` – rebuild the project

``make lint`` – run code linting (mypy)

``make test`` – run tests

``make log`` – see container logs

``make ps`` – see running containers
