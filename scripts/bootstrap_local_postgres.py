#!/usr/bin/env python3
"""Bootstrap local PostgreSQL role/database without requiring psql binary."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

try:
    import psycopg
    from psycopg import sql
except Exception as exc:  # pragma: no cover
    print(f"psycopg import failed: {exc}", file=sys.stderr)
    sys.exit(1)


def env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else default


def main() -> int:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

    db_name = env("POSTGRES_DB", "invtech")
    db_user = env("POSTGRES_USER", "invtech")
    db_password = env("POSTGRES_PASSWORD", "invtech")

    admin_user = env("PGADMIN_USER", "postgres")
    admin_password = env("PGADMIN_PASSWORD", "")
    admin_host = env("PGADMIN_HOST", env("POSTGRES_HOST", "localhost"))
    admin_port = env("PGADMIN_PORT", env("POSTGRES_PORT", "5432"))

    conn_kwargs = {
        "dbname": "postgres",
        "user": admin_user,
        "host": admin_host,
        "port": admin_port,
        "connect_timeout": int(env("POSTGRES_CONNECT_TIMEOUT", "5") or "5"),
    }
    if admin_password:
        conn_kwargs["password"] = admin_password

    try:
        with psycopg.connect(**conn_kwargs, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (db_user,))
                if cur.fetchone():
                    cur.execute(
                        sql.SQL("ALTER ROLE {} WITH LOGIN PASSWORD {}").format(
                            sql.Identifier(db_user),
                            sql.Literal(db_password),
                        )
                    )
                    print(f"Updated role password: {db_user}")
                else:
                    cur.execute(
                        sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
                            sql.Identifier(db_user),
                            sql.Literal(db_password),
                        )
                    )
                    print(f"Created role: {db_user}")

                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                if not cur.fetchone():
                    cur.execute(
                        sql.SQL("CREATE DATABASE {} OWNER {}").format(
                            sql.Identifier(db_name),
                            sql.Identifier(db_user),
                        )
                    )
                    print(f"Created database: {db_name}")

                cur.execute(
                    sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                        sql.Identifier(db_name),
                        sql.Identifier(db_user),
                    )
                )

        print(f"Local PostgreSQL ensured: user={db_user} db={db_name} host={admin_host}:{admin_port}")
        return 0
    except Exception as exc:
        print("Failed to bootstrap local PostgreSQL.", file=sys.stderr)
        print(
            "Tip: set PGADMIN_USER/PGADMIN_PASSWORD (and optionally PGADMIN_HOST/PGADMIN_PORT) in .env to admin credentials.",
            file=sys.stderr,
        )
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
