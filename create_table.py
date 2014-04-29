#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument(
    'file', metavar='jy_table3.json', type=str, help='Table Definition json file to load.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

ml = ML(server, {'username': username, 'password': password})
r = ml.create_table(args['file'])
if r.status_code == 200:
    # exit if error
    print "New table", r.text, "is created successfully."
else:
    print "Failed to create the new table with error", r.status_code, r.text

