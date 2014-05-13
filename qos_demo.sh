# create the queue table
python create_table.py https://admin:cariden@127.0.0.1:8443 queue_perQ.json
sleep 5
# convert planfile into CSV for data to be imported 
python import_qos.py /tmp/140509_1912_UTC.pln perQ.sql QoS_Counters
# save it in a file
python import_qos.py /tmp/140509_1912_UTC.pln perQ.sql QoS_Counters > /tmp/data_import_queue.txt
# insert the data
python import_data.py https://admin:cariden@127.0.0.1:8443 QoS_Counters /tmp/data_import_queue.txt  '2014-01-01 08:00:00'
python import_data.py https://admin:cariden@127.0.0.1:8443 QoS_Counters /tmp/data_import_queue.txt  '2014-01-01 08:15:00'
python import_data.py https://admin:cariden@127.0.0.1:8443 QoS_Counters /tmp/data_import_queue.txt  '2014-01-01 08:30:00'
python import_data.py https://admin:cariden@127.0.0.1:8443 QoS_Counters /tmp/data_import_queue.txt  '2014-01-01 08:45:00'
python import_data.py https://admin:cariden@127.0.0.1:8443 QoS_Counters /tmp/data_import_queue.txt  '2014-01-01 09:00:00'
# explore table
python explore.py -count 100 -properties 'node,interface,queue,TraffIn,TraffOut,PacketsIn,PacketsOut,ErrorsPacketsIn,DroppedPacketsOut' https://admin:cariden@127.0.0.1:8443 QoS_Counters
# explore time series data
python time-series.py https://admin:cariden@127.0.0.1:8443 QoS_Counters PacketsIn 'er1.van|ge-0/1/0.0|best-effort' 000101_0000_UTC 150101_0000_UTC
python time-series.py https://admin:cariden@127.0.0.1:8443 QoS_Counters TraffIn 'er1.tor|ge-2/0/7|network-control' 000101_0000_UTC 150101_0000_UTC
# drop the custom table
python drop_table.py https://admin:cariden@127.0.0.1:8443 QoS_Counters 
