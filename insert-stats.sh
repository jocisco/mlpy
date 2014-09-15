#!/bin/bash

# use the following to cron this task
# */5 * * * * /home/cariden/mlpy/insert-stats.sh > /tmp/insert-stats.log

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

source test.rc

server=https://admin:cariden@127.0.0.1:8443
table_name=ServerPerf

bash data/demo-server-perf/stats.sh  > /tmp/server.tsv

echo csv file:
cat /tmp/server.tsv

date=`date -u "+%Y-%m-%d %H:%M:00"`
date1=`date -u "+%y%m%d_%H%M_UTC" -d "10 mins ago"`
date2=`date -u "+%y%m%d_%H%M_UTC"`

# insert the data
$python ./import_data.py $server $table_name /tmp/server.tsv  -timestamp "$date"

# verify
#$python explore.py $server $table_name
$python ./time-series.py $server $table_name cpu mldev01 $date1 $date2
