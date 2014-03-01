#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument('-filename', help='Destination filename')
parser.add_argument('-dir', help='Destination directory')
parser.add_argument('-timestamp', help='YYMMDD_HHMM_ZZZ')
# TODO: add a timestamp option

args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

ml = ML(server, {'username': username, 'password': password})

plan = ml.get_plan(args['timestamp'])

if args['dir']:
    dir = args['dir'] + "/"
else:
    dir = "./"

if plan['timestamp']:  # we retrieved something
    if args['filename']:
        path = dir + args['filename']
    else:
        path = dir + plan['timestamp'] + ".pln"
    data = plan['file-content']
    with open(path, 'w') as f:
        f.write(data)
    print "File saved to " + path + "."
else:
    print "No plan file retrieved."
    sys.exit(1)
