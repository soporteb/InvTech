# Institutional IT Asset Inventory System (Phase 1)

## Stack
- Python 3.12+
- Django 5.x
- PostgreSQL
- Docker Compose

## Apps
- accounts
- core
- employees
- assets
- assignments
- consumables

## Run with Docker
1. Copy env: `cp .env.example .env`
2. Start services: `docker compose up --build`
3. Run migrations: `docker compose exec web python manage.py migrate`
4. Seed catalogs: `docker compose exec web python manage.py seed_initial_data`
5. (Optional) create admin: `docker compose exec web python manage.py createsuperuser`

## Local run (without Docker)
1. Install dependencies: `pip install -r requirements.txt`
2. Set `DJANGO_SETTINGS_MODULE=config.settings.dev`
3. Run migrations: `python manage.py migrate`
4. Seed catalogs: `python manage.py seed_initial_data`
5. Start server: `python manage.py runserver`
