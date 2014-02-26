#!/usr/bin/python

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# get_last_report - print the last job's csv data for a report
# 
# History:
#   - 02/11/13      Jonathan Garzon     initial version
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ML import ML, parse_url
import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument('url', metavar='http[s]://username:password@server', type=str,
                help='url: http[s]://username:password@server.')
parser.add_argument('did', metavar='did', type=str,
                help='Report definitionId.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError,TypeError) as e:
    print "invalid url"
    sys.exit(1)


ml = ML(server, {'username': username, 'password': password})
print ml.get_last_csv(args['did'])
