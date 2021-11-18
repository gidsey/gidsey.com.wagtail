#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py update_index

gunicorn gidsey.wsgi --bind=0.0.0.0:80 --timeout 10000 -w 3

