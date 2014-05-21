#!/usr/bin/python

from ML import ML, parse_url
import argparse
import sys

import sqlite3
import zipfile 
import re 

parser = argparse.ArgumentParser()
parser.add_argument(
    'plan-file', metavar='plan-file', type=str, help='Plan file to extract the data.')
parser.add_argument(
    'sql-file', metavar='sql-file', type=str, help='SQL file to be used.')
parser.add_argument(
    'table-name', metavar='table-name', type=str, help='Table name for these data to be inserted to.')
args = vars(parser.parse_args())


with zipfile.ZipFile(args['plan-file'], "r") as z:
    z.extractall("/tmp")
conn = sqlite3.connect('/tmp/network.db')
c = conn.cursor()
fh = open(args['sql-file'], "r+")
sql = fh.read()
col_head = ''
for col in re.finditer('as \'(.*)\'',sql):
    col_head += col.group(1)
    col_head += '\t' 
print col_head
for row in c.execute(sql):
    line = ''
    for value in row:
	# hacked due to missing data
	if str(value) == 'None':
	    line += '0'
	else:
	    line +=  str(value)
	line += '\t'
    print line
conn.close()

