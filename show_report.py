#!/usr/bin/python
import argparse
import sys
import time

from ML import ML, parse_url


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument('jid', metavar='did', type=str, help='Report JobId.')
parser.add_argument('-columns', default=None, help='Comma-delimited list of columns to display.')
parser.add_argument('-csv', help='Display in csv mode.', action='store_true')
parser.add_argument('-count', help='Number of rows to display', default=10)
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

myml = ML(server, {'username': username, 'password': password})
if args['columns']:
    columns = map(int, args['columns'].split(","))
else:
    columns = None
r = myml.get_report(args['jid'], columns)
if args['csv']:
    r.print_csv()
else:
    r.print_col()
