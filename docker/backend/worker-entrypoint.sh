#!/bin/sh

until cd /app/backend/review_project
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A review_project worker --loglevel=info --concurrency 1 -E

