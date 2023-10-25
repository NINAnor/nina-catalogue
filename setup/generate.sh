#!/bin/bash

set -eEuo pipefail

function generate_password() {
    shuf -er -n32  {A..Z} {a..z} {0..9} | tr -d '\n'
}

if [ -f "$DESTINATION/docker" ]
then
    >&2 echo "Using existing Docker secrets."
else
    >&2 echo "Generating new Docker secrets..."
    cat <<-EOF > "$DESTINATION/docker"
	POSTGRES_PASSWORD="$(generate_password)"
	DJANGO_SECRET_KEY="$(generate_password)"
	EOF
fi

source "$DESTINATION/docker"

>&2 echo "Setup completed."
