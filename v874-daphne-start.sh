#!/bin/bash

NAME="dtr4_app"
DJANGODIR=/var/www/www.elligue.com/dtr4
SOCKFILE=/var/www/www.elligue.com/run/daphne.sock
USER=cst
GROUP=cst
# NUM_WORKERS=3  # = 2 * number of cores + 1 worker
# NUM_THREADS=4
DJANGO_SETTINGS_MODULE=dtr4.settings
DJANGO_WSGI_MODULE=dtr4.asgi

echo "Starting $NAME as `whoami`..."

cd ${DJANGODIR}
source ../venv/bin/activate
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

RUNDIR=$(dirname ${SOCKFILE})
test -d ${RUNDIR} || mkdir -p ${RUNDIR}

exec ../venv/bin/daphne ${DJANGO_WSGI_MODULE}:channel_layer -u=unix:${SOCKFILE}

#    --access-log=/var/log/supervisor/dtr4_daphne_access.log
#  --name=$NAME          \
#  --user=$USER          \
#  --group=$GROUP        \
#  --log-level=debug     \
#  --log-file=-

#  --workers $NUM_WORKERS \
#  --threads $NUM_THREADS \

exec ./manage.py runworker
exec ./manage.py runworker
exec ./manage.py runworker


# daphne [-h] [-p PORT] [-b HOST] [-u UNIX_SOCKET] [--fd FILE_DESCRIPTOR]
#              [-v VERBOSITY] [-t HTTP_TIMEOUT] [--access-log ACCESS_LOG]
#              [--ping-interval PING_INTERVAL] [--ping-timeout PING_TIMEOUT]
#              [--ws-protocol [WS_PROTOCOLS [WS_PROTOCOLS ...]]]
#              [--root-path ROOT_PATH]
#              channel_layer
