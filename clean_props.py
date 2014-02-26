#!/usr/bin/python

### CHANGE ME ###
server="https://mldev01:8443"
username="admin"
password="cariden"
#################


from ML import ML

ml = ML(server, {'username': username, 'password': password})
ml.clear_props()
