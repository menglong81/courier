#!/bin/bash
cd /home/q/www/courier
if [[ -a "pidfile" ]]
then
    kill -9 `cat pidfile`
    rm -fv pidfile
fi
echo "stop done"
