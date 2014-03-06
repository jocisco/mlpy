#!/bin/bash

source test.rc

if [[ $1 ]]; then # print mode
    python=echo; 
    set +x
else
    set -x
    set -e
fi

$python ./dump_last_report_csv.py $read_server 32
$python ./dump_props.py $read_server > $props_file; cat $props_file
$python ./dump_myreports.py $read_server > $reportsdef_file; cat $reportsdef_file
$python ./explore.py $read_server LSPs -filter 'ActualPath(AP_HK_BB1|ae0.0)' -properties SourceNode,ActualPath,SetupBW,Traff -count 5
$python ./get_plan.py $write_server -dir /tmp
$python ./time-series.py $read_server Interfaces TraffIn 'AM_LA_BB2|TenGigE0/2/2' 130719_0000_UTC 130719_0200_UTC 
$python ./show_report.py $read_server -columns 1,2,3 1 -csv

$python ./clean_myreports.py $write_server
$python ./clean_props.py $write_server
$python ./load_myreports.py $write_server $reportsdef_file
$python ./load_props.py $write_server $props_file
$python ./run_myreports.py $write_server
