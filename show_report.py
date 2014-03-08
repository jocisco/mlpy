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
parser.add_argument('-count', help='Number of rows to display', default=100)
parser.add_argument('-filtered', help='Use report output filters.', action='store_true')
args = parser.parse_args()

try:
    (username, password, server) = parse_url(args.url)
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

myml = ML(server, {'username': username, 'password': password})
columns = map(int, args.columns.split(",")) if args.columns else None
# columns = map(int, args.columns.split(",")) if args.columns else None
if not args.filtered:
    r = myml.get_report(args.jid, columns, args.count)
else:
    r = myml.get_filtered_report(args.jid, columns, args.count)
if args.csv:
    r.print_csv()
else:
    r.print_col()
