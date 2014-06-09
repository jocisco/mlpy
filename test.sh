#!/bin/bash

source test.rc

if [[ $1 ]]; then # print mode
    python=echo; 
    set +x
else
    set -x
    set -e
fi

$python ./dump_last_report_csv.py $read_server $definition_id
$python ./dump_props.py $read_server > $props_file; cat $props_file
$python ./dump_myreports.py $read_server > $reportsdef_file; cat $reportsdef_file
$python ./explore.py $read_server LSPs -filter $explore_filter -properties SourceNode,ActualPath,SetupBW,Traff -count 5
$python ./get_plan.py $read_server -dir /tmp
$python ./time-series.py $read_server Interfaces TraffIn $time_series_keys $time_series_date1 $time_series_date2
$python ./show_report.py $read_server -columns 1,2,3 1 -csv
$python ./show_report.py $read_server $job_id -filtered

$python ./clean_myreports.py $write_server
$python ./clean_props.py $write_server
$python ./load_props.py $write_server $props_file
$python ./load_myreports.py $write_server $reportsdef_file
$python ./run_myreports.py $write_server
