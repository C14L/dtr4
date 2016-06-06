#!/bin/bash

NAME="dtr4_app"
DJANGODIR=/var/www/www.elligue.com/dtr4
SOCKFILE=/var/www/www.elligue.com/run/gunicorn.sock
USER=cst
GROUP=cst
NUM_WORKERS=5
DJANGO_SETTINGS_MODULE=dtr4.settings
DJANGO_WSGI_MODULE=dtr4.wsgi

echo "Starting ${NAME} as `whoami`..."

cd ${DJANGODIR}
source ../venv/bin/activate
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

RUNDIR=$(dirname ${SOCKFILE})
test -d ${RUNDIR} || mkdir -p ${RUNDIR}

exec ../venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name ${NAME} --workers ${NUM_WORKERS} \
  --user=${USER} --group=${GROUP} \
  --bind=unix:${SOCKFILE} --log-level=debug --log-file=-
