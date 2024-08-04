#!/bin/sh

cd bimebazar_web
python manage.py migrate
cd ..

exec "$@"
