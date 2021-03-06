#!/usr/bin/env bash
nohup /usr/local/openjdk-8/bin/java -jar icici-0.0.1.jar & 
set -e

echo "${0}: running migrations."
python manage.py makemigrations --merge
python manage.py migrate --noinput

echo Starting Gunicorn.
exec gunicorn --bind 0.0.0.0:80 payout.wsgi
