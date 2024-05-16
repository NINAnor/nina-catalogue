#!/bin/bash

alias dpcli_dev="export HOSTNAME && docker compose --profile dev --env-file secrets/docker"
alias dpcli_prod="export HOSTNAME && docker compose --profile prod --env-file secrets/docker"

alias djcli_dev="export HOSTNAME && docker compose --profile dev --env-file secrets/docker exec -it django-dev python manage.py"
alias djcli_prod="export HOSTNAME && docker compose --profile prod --env-file secrets/docker exec -it django python manage.py"
