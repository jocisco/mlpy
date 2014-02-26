#!/usr/bin/python

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# get_last_report - print the last job's csv data for a report
# 
# History:
#   - 02/11/13      Jonathan Garzon     initial version
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### CHANGE ME ###
server="https://mate-nvsdemo.cisco.com:8443"
username="mate"
password="matesw"
did="32" # Can be determined for the "report history" page (add definitionId column to the table)
#################

from ML import ML

ml = ML(server, {'username': username, 'password': password})
print ml.get_last_csv(did)
