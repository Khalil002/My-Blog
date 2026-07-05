#!/bin/sh
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py createsuperuser --noinput || true

if [ "$GENERATE_SAMPLE_POSTS_AND_COMMENTS" = "True" ]; then
    echo "Generating sample posts and comments..."
    python generate_posts.py
fi

if [ "$LOCAL" = "True" ]; then
    echo "Starting development server..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Starting production server..."
    exec gunicorn django_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
