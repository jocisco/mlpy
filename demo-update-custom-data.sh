#!/bin/bash                                                                                                                                                                                    

source test.rc

if [[ $1 ]]; then # print mode
    python=echo;
    set +x
else
    set -x
    set -e
fi

# create a new table with xml
$python ./create_table.py $write_server data/demo-update-custom-data/table.xml
# import data
$python ./import_data.py $write_server demo data/demo-update-custom-data/data_import_table.txt  
# explore
$python ./explore.py $write_server demo
# add new series columns in existing custom table with xml
$python ./add_columns.py $write_server demo data/demo-update-custom-data/update_table.xml
# import data for new series columns
$python ./import_data.py $write_server demo data/demo-update-custom-data/data_import_new_series.txt
# explore
$python ./explore.py $write_server demo 
# activate/inactivate existing column 
$python ./update_column.py $write_server demo tsName5 false
# explore
$python ./explore.py $write_server demo 
# drop a table
$python ./drop_table.py $write_server demo
