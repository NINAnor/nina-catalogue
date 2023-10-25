#!/bin/bash

dpcli_dev () {
    sh -c "docker compose --profile local --env-file secrets/docker $*";
}

dpcli_prod () {
    sh -c "docker compose --profile prod --env-file secrets/docker $*";
}

djcli_dev () {
    sh -c "docker compose --profile local --env-file secrets/docker exec -it django-dev python manage.py $*";
}

djcli_prod () {
    sh -c "docker compose --profile prod --env-file secrets/docker exec -it django-dev python manage.py $*";
}
