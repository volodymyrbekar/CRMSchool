#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
if [ "$DEBUG" == "True" ]; then
    echo "WARNING: DEBUG is set to True! This is not recommended for production."
    # Start the application using Django's runserver
    python manage.py runserver 0.0.0.0:8000
else
    # Start the application using Gunicorn in production mode
    echo "Starting the application in production mode..."
    gunicorn crmschool.wsgi:application --bind 0.0.0.0:8000
fi
