#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument('object', metavar='object', help='Interfaces|LSPs|Nodes|Demands')
parser.add_argument('-filter', help='MATE Live filter')
parser.add_argument('-properties', help='Comma-delimited list of propeties.')
parser.add_argument('-csv', help='Display in csv mode.', action='store_true')
parser.add_argument('-count', default=10, help='Count of objects to display.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

myml = ML(server, {'username': username, 'password': password})
#r = myml.explore(args['object'], args['filter'], 100, {'SetupBW', 'SourceNode'})
if args['properties']:
    properties = args['properties'].split(",")
else:
    properties = None
r = myml.explore(args['object'], args['filter'], args['count'], properties)
if args['csv']:
    r.print_csv()
else:
    r.print_col()
