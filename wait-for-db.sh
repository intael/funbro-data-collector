#!/bin/bash

set -e
shift
cmd="$*"

echo "$cmd"


until PGPASSWORD=$POSTGRES_DATABASE_PASSWORD_FIELD psql -h "$POSTGRES_DATABASE_HOST_FIELD" -U "$POSTGRES_DATABASE_USER_FIELD" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

>&2 echo "Postgres is up - executing command"
exec $cmd
