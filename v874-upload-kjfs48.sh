#!/bin/bash

SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DST="cst@89.110.147.123:/var/www/www.elligue.com/"

echo "${SRC} >>> ${DST}"
read -rsp "Press [ENTER] to start..."

#chmod -R 755 ${SRC}

rsync -rtvP --delete --exclude=app/ --exclude=*.pyc --exclude=*/__pycache__ ${SRC} ${DST}
