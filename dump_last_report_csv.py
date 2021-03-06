#!/usr/bin/python

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# get_last_report - print the last job's csv data for a report
#
# History:
#   - 02/11/13      Jonathan Garzon     initial version
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ML import ML, parse_url
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument('did', metavar='did', type=str, help='Report definitionId.')
parser.add_argument('-filtered', help='Use report output filters.', action='store_true')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)


ml = ML(server, {'username': username, 'password': password})
filtered = args['filtered']

jid = ml.last_job(args['did'])

if filtered:
    ml.get_filtered_report(jid, filtered, count=1000000).print_csv()
else:
    print ml.get_csv_file(jid)
