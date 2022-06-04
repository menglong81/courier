#!/bin/bash
cd /home/q/www/courier
if [[ ! -e pidfile ]]
then
    gunicorn -w 1 -k gevent -b 0.0.0.0:8080 DjangoProject.courier_wsgi -D --pid pidfile
fi
ps auxf | grep courier | grep -v grep
echo "start done"
