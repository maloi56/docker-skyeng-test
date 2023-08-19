# pull official base image
FROM python:3.11

RUN apt-get update && \
    apt-get install -y python3-dev gcc libc-dev libfreetype6

WORKDIR /app

RUN pip install --upgrade pip
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./src /app/backend
ADD ./docker /app/docker

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
RUN chmod +x /app/docker/backend/celerybeat-entrypoint.sh
