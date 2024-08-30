#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start the application
echo "Starting the application..."
python manage.py runserver 0.0.0.0:8000