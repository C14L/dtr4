#!/bin/bash

DJANGODIR=/var/www/www.elligue.com/dtr4
DJANGO_SETTINGS_MODULE=dtr4.settings

echo "Starting workers..."

cd ${DJANGODIR}
source ../venv/bin/activate
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

exec python ${DJANGODIR}/manage.py runworker
