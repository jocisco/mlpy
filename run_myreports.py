#!/usr/bin/python

### CHANGE ME ###
server="https://mldev01:8443"
username="admin"
password="cariden"
#################

import sys
from time import sleep
from datetime import datetime

from ML import ML
ml = ML(server, {'username': username, 'password': password})

myreports = ml.my_reports()

print "-" * 98
sys.stdout.write('| {:50s} | {:4s} | {:4s} | {:10s} | {:14s} |\n'.format("name", "did", "jid", "status", "time"))
print "-" * 98

total_time = None
for report in myreports:
    did = str(report["definitionId"])
    name = report["definitionName"]

    # run
    start = datetime.now()
    jid=ml.run_report(did);

    status="running"
    # get status
    while (status == "running") or (status == "created") : 
        sleep(1)
        try:
            status = ml.get_job_status(jid)
        except:
            print status, "<error>"
        diff = datetime.now() - start
        sys.stdout.write('| {:50s} | {:4s} | {:4s} | {:10s} | {:14s} |\r'.format(name, did, jid, status, str(diff)))
        sys.stdout.flush()
    sys.stdout.write('| {:50s} | {:4s} | {:4s} | {:10s} | {:14s} | '.format(name, did, jid, status, str(diff)))
    try:
        sys.stdout.write(str(len(ml.get_csv(jid))/(8*8*8))+" (KB)")
    except:
        pass
    print
    if total_time != None:
        total_time=total_time+diff
    else:
        total_time=diff

print "-" * 98
print "total time: " + str(total_time)
