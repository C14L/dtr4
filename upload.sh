#!/bin/bash

SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DST="cst@89.110.146.104:/opt/elligue/"

echo "${SRC} >>> ${DST}"
read -rsp "Press [ENTER] to start..."

#chmod -R 755 ${SRC}

rsync -rtvP --delete --exclude=*.pyc --exclude=www --exclude=*/__pycache__ ${SRC} ${DST}
rsync -rtvP --delete ${SRC}/www ${DST}
