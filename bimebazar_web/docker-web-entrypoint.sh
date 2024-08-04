#!/bin/sh

cd /code/bimebazar_web
python manage.py migrate
cd /code

exec "$@"
