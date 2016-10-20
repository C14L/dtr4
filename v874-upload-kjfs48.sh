#!/bin/bash

SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DST="cst@89.110.147.123:/var/www/www.elligue.com/"

echo "${SRC} >>> ${DST}"
read -rsp "Press [ENTER] to start..."

echo "collecting static files..."
${SRC}/manage.py collectstatic --noinput

echo "fixing any chmod problems..."
find ${SRC} -type d -print0 | xargs -0 chmod 755
find ${SRC} -type f -print0 | xargs -0 chmod 644
chmod -R 755 ${SRC}/manage.py
chmod -R 755 ${SRC}/v874-*.sh

read -rsp "Press [ENTER] to start..."

rsync -rLtvP --delete-after --exclude=db.sqlite3 --exclude=___* --exclude=app/ --exclude=*.pyc --exclude=*/__pycache__ ${SRC} ${DST}

echo 
echo "***************************************************"
echo "**                                               **"
echo "**     !! Now restart "dtr4" on the server!!     **"
echo "**                                               **"
echo "**                                               **"
echo "**   root@server:~# supervisorctl restart dtr4   **"
echo "**                                               **"
echo "***************************************************"
echo

