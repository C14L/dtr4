#!/bin/bash

NAME="dtr4_app"
USER=cst
GROUP=cst

DJANGODIR=/var/www/www.elligue.com/dtr4
DJANGO_SETTINGS_MODULE=dtr4.settings

SOCKFILE=/var/www/www.elligue.com/run/gateway.sock

echo "Starting gateway ${NAME} as `whoami`..."

cd ${DJANGODIR}
source ../venv/bin/activate
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

RUNDIR=$(dirname ${SOCKFILE})
test -d ${RUNDIR} || mkdir -p ${RUNDIR}

################################################################################
### GUNICORN ###################################################################   !!!!!!!!!!!!!!!!!!!!!! TOOO: IN PROGRESS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
################################################################################

DJANGO_WSGI_MODULE=dtr4.wsgi

NUM_WORKERS=1  # total workers, ~ 2-4 x number of cores
NUM_THREADS=4  # threads per worker, ~ 2-4 x number of cores

exec ../venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name ${NAME} \
  --workers ${NUM_WORKERS} \
  --threads ${NUM_THREADS} \
  --user=${USER} \
  --group=${GROUP} \
  --bind=unix:${SOCKFILE} \
  --log-level=debug --log-file=-

################################################################################
### DAPHNE #####################################################################
################################################################################

#DJANGO_WSGI_MODULE=dtr4.asgi
#
#exec ${DJANGODIR}/../venv/bin/daphne ${DJANGO_WSGI_MODULE}:channel_layer -u=unix:${SOCKFILE}

# daphne [-h] [-p PORT] [-b HOST] [-u UNIX_SOCKET] [--fd FILE_DESCRIPTOR]
#              [-v VERBOSITY] [-t HTTP_TIMEOUT] [--access-log ACCESS_LOG]
#              [--ping-interval PING_INTERVAL] [--ping-timeout PING_TIMEOUT]
#              [--ws-protocol [WS_PROTOCOLS [WS_PROTOCOLS ...]]]
#              [--root-path ROOT_PATH]
#              channel_layer
