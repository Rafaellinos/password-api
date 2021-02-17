#!/bin/bash

alembic -c /alembic.ini upgrade head
exec python /app/main.py