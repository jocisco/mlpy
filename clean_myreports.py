#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

ml = ML(server, {'username': username, 'password': password})
ml.flush_myreports()
