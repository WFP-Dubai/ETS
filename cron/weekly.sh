#!/bin/sh

PIDFILE="./cron/weekly.pid"

if test -r $PIDFILE ; then

  if $(kill -CHLD `cat $PIDFILE` >/dev/null 2>&1) ; then
    echo "pid is alive, exiting"
    exit 0
  else
    echo "pid is dead, continue"
  fi

fi
echo $$ > $PIDFILE

#Update full data from COMPAS station
./bin/instance import_compas_full --compas="ISBX002" 2>&1

rm -f $PIDFILE
