#!/bin/bash

set -x
set -e

./dump_last_report_csv.py https://mate:matesw@mate-nvsdemo.cisco.com:8443 32
./dump_props.py https://mate:matesw@mate-nvsdemo.cisco.com:8443 | tee props.txt
./dump_myreports.py https://mate:matesw@mate-nvsdemo.cisco.com:8443 | tee reports.txt
./clean_myreports.py https://admin:cariden@mldev01:8443
./clean_props.py https://admin:cariden@mldev01:8443
./load_myreports.py https://admin:cariden@mldev01:8443 reports.txt
./load_props.py https://admin:cariden@mldev01:8443 props.txt
./run_myreports.py https://admin:cariden@mldev01:8443
