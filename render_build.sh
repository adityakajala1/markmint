#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running Alembic schema migrations..."
alembic upgrade head

echo "Populating production database from SQLite backup..."
# The script is idempotent; it skips if data already exists
python scripts/migrate_sqlite_to_pg.py sqlite:///./production_corpus.db "$DATABASE_URL"

echo "Build and migration step completed successfully."
