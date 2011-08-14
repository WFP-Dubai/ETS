#!/bin/sh

PIDFILE="./cron/daily.pid"

if test -r $PIDFILE ; then

  if $(kill -CHLD `cat $PIDFILE` >/dev/null 2>&1) ; then
    echo "pid is alive, exiting"
    exit 0
  else
    echo "pid is dead, continue"
  fi

fi
echo $$ > $PIDFILE

echo "Synchronize with compas database"
./bin/instance sync_compas --verbosity=2 2>&1

rm -f $PIDFILE
