#!/bin/bash

set -o errexit
set -o pipefail

python manage.py wait_for_database

if [[ -z "${WAIT_FOR_HTTP}" ]]
then
  echo "No HTTP service to wait for"
else
  python manage.py wait_for_http "$WAIT_FOR_HTTP"
fi

if [[ -z "${DJANGO_MIGRATE}" ]]
then
  echo "Skip migration and setup"
else
  python manage.py migrate
  python manage.py setup
fi

if [[ -z "${DJANGO_TAILWIND}" ]]
then
  echo "Skip tailwind"
else
  python manage.py tailwind install --no-input
fi

if [[ -z "${DJANGO_COLLECTSTATIC}" ]]
then
  echo "Skip collectstatic"
else
  python manage.py collectstatic --noinput
fi

exec "$@"
