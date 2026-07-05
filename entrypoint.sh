#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py createsuperuser --noinput || true

if [ "$GENERATE_SAMPLE_POSTS_AND_COMMENTS" = "True" ]; then
    echo "Generating sample posts and comments..."
    python generate_posts.py
fi

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
