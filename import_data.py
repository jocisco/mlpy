#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument(
    'table', metavar='table', type=str, help='The custom table to import data into.')
parser.add_argument(
    'file', metavar='data_file', type=str, help='Custom data file to import.')
parser.add_argument(
    '-timestamp', metavar='timestamp', type=str, help='timestamp for import.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

ml = ML(server, {'username': username, 'password': password})
r = ml.import_data(args['table'],args['file'], args['timestamp'])
if r.status_code != 201:
    # exit if error
    print "Failed to submit the job to import data with error ", r.status_code, r.text
    sys.exit(1)
else:
    job_id = r.text
    print "Data import job is scheduled with job id = ", job_id
    i = 0	
    while (i<10):
        print "Check every 2 seconds to see if the job is complete."
        status = ml.scheduler_job_status(job_id)
	if status == 'COMPLETED':
	    break
 	else:
	    i += 1
	    time.sleep(2)
    print "job status from data import is ", status 
