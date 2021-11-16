#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn gidsey.wsgi --bind=0.0.0.0:80 --timeout 10000 -w 3

