#!/usr/bin/python

### CHANGE ME ###
server="https://mldev01:8443"
username="admin"
password="cariden"
#################

import json
from ML import ML

ml = ML(server, {'username': username, 'password': password})
ml.load_myreports_from_file("reports.txt")
