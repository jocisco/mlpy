#!/bin/bash

source test.rc

if [[ $1 ]]; then # print mode
    python=echo; 
    set +x
else
    set -x
    set -e
fi

table_name=ServerPerf

# create the queue table
$python ./create_table.py $write_server data/demo-server-perf/table.json

bash data/demo-server-perf/stats.sh  > /tmp/server.tsv

# insert the data
$python ./import_data.py $write_server $table_name /tmp/server.tsv  -timestamp "`date -u "+%Y-%m-%d %H:%M:00"`"

# explore table
$python ./explore.py -count 100 $write_server $table_name
# explore time series data
#$python ./time-series.py $write_server $table_name PacketsIn 'er1.van|ge-0/1/0.0|best-effort' 000101_0000_UTC 150101_0000_UTC -keyColumns 'node,interface,queue'

# drop the custom table
read -p "Press [Enter] key to delete the table..."
$python ./drop_table.py $write_server $table_name 
