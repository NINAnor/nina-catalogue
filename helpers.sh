#!/bin/bash

alias dpcli_dev="docker compose --profile dev --env-file secrets/docker"
alias dpcli_prod="docker compose --profile prod --env-file secrets/docker"

alias djcli_dev="docker compose --profile dev --env-file secrets/docker exec -it django-dev python manage.py"
alias djcli_prod="docker compose --profile prod --env-file secrets/docker exec -it django-dev python manage.py"
