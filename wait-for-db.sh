#!/bin/sh

set -e

# Start PostgreSQL if it's not already running
if ! pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; then
    echo "PostgreSQL is not running - starting PostgreSQL"
    service postgresql start
else
    echo "PostgreSQL is already running"
fi

# Wait until PostgreSQL is fully ready
until pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; do
    echo "PostgreSQL is still starting - sleeping"
    sleep 1
done

# Execute the command
echo "Starting Django server"
exec "$@"
