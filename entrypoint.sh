#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start the application
echo "Starting the application..."
#gunicorn  crmschool.wsgi:application --bind 0.0.0.0:8000  # replace 0.0.0.0 -> 161.35.66.41
python manage.py runserver 0.0.0.0:8000
