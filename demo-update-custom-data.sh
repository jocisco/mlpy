# create a new table with xml
python create_table.py https://admin:cariden@127.0.0.1:8443 data/demo-update-custom-data/table.xml
# import data
python import_data.py https://admin:cariden@127.0.0.1:8443 demo data/demo-update-custom-data/data_import_table.txt  
# explore
python explore.py https://admin:cariden@127.0.0.1:8443 demo
# add new series columns in existing custom table with xml
python add_columns.py https://admin:cariden@127.0.0.1:8443 demo data/demo-update-custom-data/update_table.xml
# import data for new series columns
python import_data.py https://admin:cariden@127.0.0.1:8443 demo data/demo-update-custom-data/data_import_new_series.txt
# explore
python explore.py https://admin:cariden@127.0.0.1:8443 demo 
# activate/inactivate existing column 
python update_column.py https://admin:cariden@127.0.0.1:8443 demo tsName5 false
# explore
python explore.py https://admin:cariden@127.0.0.1:8443 demo 
# drop a table
python drop_table.py https://admin:cariden@127.0.0.1:8443 demo
