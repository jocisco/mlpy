#!/bin/bash

source test.rc

if [[ $1 ]]; then # print mode
    python=echo; 
    set +x
else
    set -x
    set -e
fi

table_name=InterfaceQueues

# create the queue table
$python ./create_table.py $write_server data/demo-qos-proto/queue_perQ.json
# convert planfile into CSV for data to be imported 
$python ./import_qos.py data/demo-qos-proto/140509_1912_UTC.pln data/demo-qos-proto/perQ.sql $table_name
# save it in a file
$python ./import_qos.py data/demo-qos-proto/140509_1912_UTC.pln data/demo-qos-proto/perQ.sql $table_name > /tmp/data_import_queue.txt
# insert the data
$python ./import_data.py $write_server $table_name /tmp/data_import_queue.txt  -timestamp '2014-01-01 08:00:00'
$python ./import_data.py $write_server $table_name /tmp/data_import_queue.txt  -timestamp '2014-01-01 08:15:00'
$python ./import_data.py $write_server $table_name /tmp/data_import_queue.txt  -timestamp '2014-01-01 08:30:00'
$python ./import_data.py $write_server $table_name /tmp/data_import_queue.txt  -timestamp '2014-01-01 08:45:00'
$python ./import_data.py $write_server $table_name /tmp/data_import_queue.txt  -timestamp '2014-01-01 09:00:00'
# explore table
# should work when DE94 is fixed
#$python ./explore.py -count 100 -properties 'node,interface,queue,TraffIn,TraffOut,PacketsIn,PacketsOut,ErrorsPacketsIn,DroppedPacketsOut' $write_server $table_name
$python ./explore.py -count 100 $write_server $table_name
# explore time series data
$python ./time-series.py $write_server $table_name PacketsIn 'er1.van|ge-0/1/0.0|best-effort' 000101_0000_UTC 150101_0000_UTC -keyColumns 'node,interface,queue'
$python ./time-series.py $write_server $table_name TraffIn 'er1.tor|ge-2/0/7|network-control' 000101_0000_UTC 150101_0000_UTC -keyColumns 'node,interface,queue'
# drop the custom table
read -p "Press [Enter] key to delete the table..."
$python ./drop_table.py $write_server $table_name 
