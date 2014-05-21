#!/bin/bash

source test.rc

if [[ $1 ]]; then # print mode
    python=echo;
    set +x
else
    set -x
    set -e
fi

# create a new table with json
$python ./create_table.py $write_server data/demo-custom-data/table2.json
# create a new table with xml
# $python create_table.py $write_server data/demo-custom-data/table3.xml
# import data

# jgarzon 5/20/14: temporary workaround
cp data/demo-custom-data/data_import2.txt /tmp/data_import2.txt
$python ./import_data.py $write_server demo /tmp/data_import2.txt  
# explore
$python ./explore.py $write_server demo 
# explore time series data
$python ./time-series.py $write_server demo tsName1 nodeA-B-C 000101_0000_UTC 150101_0000_UTC
# drop a table
$python ./drop_table.py $write_server demo 
