#!/bin/sh

until cd /app/backend/review_project
do
    echo "Waiting for server volume..."
done

# run a celerybeat :)

celery -A review_project beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
