#!/usr/bin/python

from ML import ML, parse_url
import argparse, sys
import json

parser = argparse.ArgumentParser()
parser.add_argument('url', metavar='http[s]://username:password@server', type=str,
                help='url: http[s]://username:password@server.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError,TypeError) as e:
    print "invalid url"
    sys.exit(1)

ml = ML(server, {'username': username, 'password': password})
print json.dumps(ml.my_reports_definitions(), indent=4)
