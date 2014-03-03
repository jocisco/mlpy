#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys
import json
from time import sleep
from datetime import datetime

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument('-non-interactive', help='Suitable for script output.', action='store_true', default=False)
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

ml = ML(server, {'username': username, 'password': password})

myreports = ml.my_reports()

print "+{:s}+".format("-" * 96)
sys.stdout.write('| {:50s} | {:4s} | {:4s} | {:10s} | {:14s} |\n'.format(
    "name", "did", "jid", "status", "time"))
print "+{:s}+".format("-" * 96)

total_time = None
for report in myreports:
    did = str(report["definitionId"])
    name = report["definitionName"]

    # run
    start = datetime.now()
    jid = ml.run_report(did)

    status = "running"
    # get status
    while (status == "running") or (status == "created"):
        sleep(1)
        try:
            status = ml.job_status(jid)
        except:
            sys.stdout.write("{:s} <error retrieving job status>\r".format(status))
        diff = datetime.now() - start
        if not args['non_interactive']:
            sys.stdout.write('| {:50s} | {:4s} | {:4s} | {:10s} | {:14s} |\r'.format(
                name, did, jid, status, str(diff)))
            sys.stdout.flush()
    sys.stdout.write('| {:50s} | {:4s} | {:4s} | {:10s} | {:14s} | '.format(
        name, did, jid, status, str(diff)))
    try:
        sys.stdout.write(str(len(ml.get_csv(jid)) / (8 * 8 * 8)) + " (KB)")
    except:
        pass
    print
    if total_time:
        total_time = total_time + diff
    else:
        total_time = diff

print "+{:s}+".format("-" * 96)
print "total time: " + str(total_time)
