# create a new table with json
python create_table.py https://admin:cariden@127.0.0.1:8443 table2.json
# create a new table with xml
python create_table.py https://admin:cariden@127.0.0.1:8443 table3.xml
# import data
python import_data.py https://admin:cariden@127.0.0.1:8443 demo data_import2.txt  
# explore
python explore.py https://admin:cariden@127.0.0.1:8443 demo 
# explore time series data
 python time-series.py https://admin:cariden@127.0.0.1:8443 demo tsName1 nodeA-B-C 000101_0000_UTC 150101_0000_UTC
# drop a table
python drop_table.py https://admin:cariden@127.0.0.1:8443 demo 
