#!/bin/bash

# Wait for postgres to be ready and accepting connections
while ! nc -z postgres12 5432; do sleep 1; done;

echo "Running migrations"
alembic -c /app/alembic.ini upgrade head

echo "Starting server"
python /app/run_uvicorn.py