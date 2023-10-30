#!/bin/bash

set -o errexit
set -o pipefail

python manage.py wait_for_database

if [ -z ${var+WAIT_FOR_HTTP} ]
then
  echo "No HTTP service to wait for"
else
  python manage.py wait_for_http "$WAIT_FOR_HTTP"
fi

if [ "$DJANGO_ENV" == "dev" ]
then
  python manage.py migrate
  python manage.py setup
else
  python manage.py collectstatic --noinput
fi

exec "$@"
