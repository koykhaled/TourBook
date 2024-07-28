# #!/usr/bin/env bash
# # Exit on error
# set -o errexit

# # Modify this line as needed for your package manager (pip, poetry, etc.)
# pip install -r requirements.txt

# # Convert static asset files
# python manage.py collectstatic --no-input

# # Apply any outstanding database migrations
# # python manage.py migrate
# #!/bin/bash

# # Apply database migrations
# echo "Applying database migrations..."
# python manage.py makemigrations
# python manage.py migrate

# # Start the application
# echo "Starting the application..."
# gunicorn TourBook.asgi:application --workers=4 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:$PORT
#!/bin/bash

# Set the necessary environment variables
export DATABASE_URL="postgresql://tourbook_ffi9_user:FEidGVybo60YCqDHN66K3pPqrU2Taxja@dpg-cqfutdpu0jms7388ker0-a/tourbook_ffi9"
export SECRET_KEY="c5e43a2e1387d147594940c43e39d7a9"
export DEBUG="False"

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Start the Django application
gunicorn TourBook.wsgi --log-file -