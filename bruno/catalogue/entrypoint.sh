#!/bin/bash

set -o errexit
set -o pipefail

if [[ -z "${WAIT_FOR_HTTP}" ]]
then
  echo "No HTTP service to wait for"
else
  ./wait-for -t 60 "$WAIT_FOR_HTTP"
fi

exec /usr/local/bin/bru run --env Docker "$@"
