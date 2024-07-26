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
#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
/opt/render/project/src/.venv/bin/python -m pip install -r requirements.txt
/opt/render/project/src/.venv/bin/python manage.py collectstatic --no-input
/opt/render/project/src/.venv/bin/python manage.py migrate

#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python manage.py collectstatic --no-input
python manage.py migrate