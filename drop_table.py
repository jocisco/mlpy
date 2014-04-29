#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument(
    'table', metavar='jy_table1', type=str, help='Table name to be dropped.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
    print "username, password, server = ", username, password, server
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

ml = ML(server, {'username': username, 'password': password})
r = ml.drop_table(args['table'])
if r.status_code == 200:
    # exit if error
    print "Table", r.text, "is deleted successfully."
else:
    print "Failed to delete the table with error", r.status_code, r.text

