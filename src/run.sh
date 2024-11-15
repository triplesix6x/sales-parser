#!/bin/bash

until pg_isready -h postgres -p 5432; do
  sleep 1
done


alembic revision --autogenerate -m "create auto-migration"
alembic upgrade head
python3.12 main.py
