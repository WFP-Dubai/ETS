#!/bin/sh

PIDFILE="./cron/hourly.pid"

if test -r $PIDFILE ; then

  if $(kill -CHLD `cat $PIDFILE` >/dev/null 2>&1) ; then
    echo "pid is alive, exiting"
    exit 0
  else
    echo "pid is dead, continue"
  fi

fi
echo $$ > $PIDFILE

echo "Count percentage of order executing"
./bin/instance order_percentage 2>&1

#Update orders and stock
./bin/instance sync_compas 2>&1

rm -f $PIDFILE
