#!/usr/bin/env bash
set -euo pipefail

if ! command -v psql >/dev/null 2>&1; then
  echo "psql is required but not found. Install PostgreSQL client tools first." >&2
  exit 1
fi

ENV_FILE=".env"
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

POSTGRES_DB="${POSTGRES_DB:-invtech}"
POSTGRES_USER="${POSTGRES_USER:-invtech}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-invtech}"
ADMIN_USER="${PGADMIN_USER:-postgres}"

export PGPASSWORD="${PGADMIN_PASSWORD:-}"

psql -U "$ADMIN_USER" -d postgres <<SQL
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${POSTGRES_USER}') THEN
      CREATE ROLE ${POSTGRES_USER} LOGIN PASSWORD '${POSTGRES_PASSWORD}';
   ELSE
      ALTER ROLE ${POSTGRES_USER} WITH LOGIN PASSWORD '${POSTGRES_PASSWORD}';
   END IF;
END
$$;
SQL

if ! psql -U "$ADMIN_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='${POSTGRES_DB}'" | grep -q 1; then
  psql -U "$ADMIN_USER" -d postgres -c "CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};"
fi

psql -U "$ADMIN_USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"

echo "Local PostgreSQL role/database ensured: user=${POSTGRES_USER} db=${POSTGRES_DB}"
