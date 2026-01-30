#!/bin/bash

set -e

echo "Running Alembic Migrations..."
alembic upgrade head

echo "Starting the app..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
