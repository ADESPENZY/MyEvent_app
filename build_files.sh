#!/usr/bin/env bash

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
