#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run Django management commands
python manage.py collectstatic --no-input
python manage.py migrate

# Seed dummy data if needed
python manage.py seed_data