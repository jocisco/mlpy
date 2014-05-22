#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument(
    'table', metavar='custom_table', type=str, help='Table name to be updated.')
parser.add_argument(
    'column', metavar='custom_table_column', type=str, help='Column name to be updated.')
parser.add_argument(
    'status', metavar='true_false', type=str, help='Activate or inactivate a given column.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

ml = ML(server, {'username': username, 'password': password})
r = ml.update_column(args['table'], args['column'], args['status'])
if r.status_code == 200:
    # exit if error
    print "Updated",args['column']," status to ",args['status'], " in ",args['table'], " successfully."
else:
    print "Failed to update column status in the custom table with error", r.status_code, r.text

