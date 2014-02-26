#!/usr/bin/python

### CHANGE ME ###
server="https://mate-nvsdemo.cisco.com:8443"
username="mate"
password="matesw"
#################

from ML import ML
import json

ml = ML(server, {'username': username, 'password': password})
print json.dumps(ml.props(), indent=4)
