# Institutional IT Asset Inventory System (Phases 1-3)

## Stack
- Python 3.12+
- Django 5.x
- PostgreSQL
- Django Templates + HTMX
- Tailwind CSS

## Run with Docker (first time)
1. `cp .env.example .env`
2. `docker compose up --build -d`
3. `docker compose exec web python manage.py migrate`
4. `docker compose exec web python manage.py seed_initial_data`
5. `docker compose exec web python manage.py createsuperuser`
6. Open `http://localhost:8000/accounts/login/`

## Run locally (first time)
1. Create and activate virtualenv.
2. `pip install -r requirements.txt`
3. Ensure PostgreSQL is running locally.
4. Keep `.env` with `POSTGRES_HOST=localhost` (default in `.env.example`).
5. Create/repair local DB + user credentials from `.env` (**no `psql` CLI required**):
   - Linux/macOS: `./scripts/bootstrap_local_postgres.sh`
   - Windows PowerShell: `./scripts/bootstrap_local_postgres.ps1`
6. `python manage.py migrate`
7. `python manage.py seed_initial_data`
8. `python manage.py createsuperuser`
9. `python manage.py runserver`

---

## ✅ Step-by-step after **every branch update**

### A) Docker workflow (after `git pull` / branch switch)
1. `git pull`
2. `docker compose down`
3. `docker compose up --build -d`
4. `docker compose exec web python manage.py migrate`
5. `docker compose exec web python manage.py seed_initial_data`
6. `docker compose exec web python manage.py test`
7. Open: `http://localhost:8000/`

If static files were changed and you use production-like serving:
8. `docker compose exec web python manage.py collectstatic --noinput`

### B) Local workflow (after `git pull` / branch switch)
1. `git pull`
2. Activate your virtualenv
3. `pip install -r requirements.txt`
4. Confirm PostgreSQL is running and `.env` is correct (`POSTGRES_HOST=localhost`)
5. Re-sync local credentials/database from `.env`:
   - Linux/macOS: `./scripts/bootstrap_local_postgres.sh`
   - Windows PowerShell: `./scripts/bootstrap_local_postgres.ps1`
6. `python manage.py migrate`
7. `python manage.py seed_initial_data`
8. `python manage.py test`
9. `python manage.py runserver`

---

## If `python manage.py migrate` fails with password authentication error
Error example: `FATAL: la autenticación password falló para el usuario 'invtech'`.

This means your local PostgreSQL user/password does not match `.env`.

1. Verify `.env` values:
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`
   - `POSTGRES_HOST=localhost`
2. Run bootstrap script to align PostgreSQL user/db/password with `.env` (uses Python + psycopg, not `psql` binary):
   - Linux/macOS: `./scripts/bootstrap_local_postgres.sh`
   - Windows PowerShell: `./scripts/bootstrap_local_postgres.ps1`
3. Retry: `python manage.py migrate`

> Note: if your PostgreSQL admin credentials are required, set these in `.env` before bootstrap:
> - `PGADMIN_USER` (default `postgres`)
> - `PGADMIN_PASSWORD`
> - `PGADMIN_HOST` (default `localhost`)
> - `PGADMIN_PORT` (default `5432`)

## If `python manage.py migrate` hangs / delays
- Verify host/port in `.env` (`POSTGRES_HOST`, `POSTGRES_PORT`).
- For local run, **do not use `POSTGRES_HOST=db`** (that value is only for Docker service-to-service).
- Connection timeout is configured with `POSTGRES_CONNECT_TIMEOUT` (default: 5s) to fail fast on unreachable DB.

## Main routes
- `/` Dashboard
- `/assets/` Assets list + HTMX filters
- `/employees/` Employees CRUD
- `/locations/` Locations CRUD
