#!/usr/bin/python
import argparse
import sys
import time

from ML import ML, parse_url


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'url', metavar='url', type=str, help='http[s]://username:password@server.')
parser.add_argument('object', metavar='object', help='Interfaces|LSPs|Nodes|Demands.')
parser.add_argument('property', help='Property.')
parser.add_argument('keys', help='"|" delimited list of keys.')
parser.add_argument('from', help='from date YYMMDD_HHMM_UTC.')
parser.add_argument('to', help='to date YYMMDD_HHMM_UTC.')
args = vars(parser.parse_args())

try:
    (username, password, server) = parse_url(args['url'])
except (ValueError, TypeError) as e:
    print "invalid url"
    sys.exit(1)

myml = ML(server, {'username': username, 'password': password})
#r = myml.explore(args['object'], args['filter'], 100, {'SetupBW', 'SourceNode'})

date_pattern = '%y%m%d_%H%M_%Z'
date_from = time.strptime(args['from'], date_pattern)
date_to = time.strptime(args['to'], date_pattern)

print myml.time_series(args['object'], args['property'], args['keys'].split("|"),
                       date_from, date_to)
#print myml.time_series("Interfaces", "TraffIn", ["AM_LA_BB2", "TenGigE0/2/2"])
