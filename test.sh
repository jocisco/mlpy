#!/bin/bash

set -x
set -e

source test.rc

$python ./dump_last_report_csv.py $read_server 32
$python ./dump_props.py $read_server > $props_file; cat $props_file
$python ./dump_myreports.py $read_server > $reportsdef_file; cat $reportsdef_file
$python ./explore.py $read_server LSPs -filter "ActualPath(AP_HK_BB1|ae0.0)" -properties SourceNode,ActualPath,SetupBW,Traff -count 5
$python ./get_plan.py $write_server -dir /tmp

$python ./clean_myreports.py $write_server
$python ./clean_props.py $write_server
$python ./load_myreports.py $write_server $reportsdef_file
$python ./load_props.py $write_server $props_file
$python ./run_myreports.py $write_server
