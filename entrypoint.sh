#!/bin/bash

alembic -c /alembic.ini upgrade head
cd /app
exec python /app/main.py