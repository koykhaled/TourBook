#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
# python manage.py migrate
#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Start the application
echo "Starting the application..."
gunicorn TourBook.asgi:application --workers=4 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:$PORT