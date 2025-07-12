#!/usr/bin/env bash
set -e

# Wait for Postgres
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -c '\q' $DB_NAME; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

# Run migrations
>&2 echo "Running migrations..."
python manage.py migrate --noinput

# Run custom command if provided, else start server
if [ "$#" -gt 0 ]; then
  exec "$@"
else
  >&2 echo "Starting Django server..."
  exec python manage.py runserver 0.0.0.0:8000
fi 