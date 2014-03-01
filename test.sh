#!/bin/bash

set -x
set -e

read_server="https://mate:matesw@mate-nvsdemo.cisco.com:8443"
write_server="https://admin:cariden@mldev01:8443"
props_file=/tmp/props.txt
reportsdef_file=/tmp/reports.txt

./dump_last_report_csv.py $read_server 32
./dump_props.py $read_server > $props_file; cat $props_file
./dump_myreports.py $read_server > $reportsdef_file; cat $reportsdef_file
./explore.py $read_server LSPs -filter "ActualPath(AP_HK_BB1|ae0.0)" -properties SourceNode,ActualPath,SetupBW,Traff -count 5
./get_plan.py $write_server -dir /tmp/

./clean_myreports.py $write_server
./clean_props.py $write_server
./load_myreports.py $write_server $reportsdef_file
./load_props.py $write_server $props_file
./run_myreports.py $write_server
