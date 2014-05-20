#!/usr/bin/python

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MATE Live python class
#
# History:
#  - 02/20/2014     Jonathan Garzon     Initial version (proof of concept)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Example code:
#
# from ML import ML
# import json
#
# ml = ML(server, {'username': username, 'password': password})
# print json.dumps(ml.my_reports_definitions(), indent=4)
import calendar
import json
import time
import urllib
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from urlparse import urlparse

import requests
import re


class ML:

    def __init__(self, server, credentials):
        self.credentials = credentials
        self.server = server
        self.cookies = self.login(credentials)

    def login(self, credentials):
        r = requests.post(self.server + "/matelive/services/auth/login",
                          data=credentials, verify=False)
        r.raise_for_status()
        self.cookies = r.cookies
        return self.cookies

    def get(self, url, get_params=None):
        headers = {'Accept': 'application/json, text/javascript, */*'}
        r = requests.get(url, cookies=self.cookies, headers=headers,
                         verify=False, params=get_params)
        return r

    def put(self, url, data):
        headers = {'Accept': 'text/plain, */*; q=0.01', 'Content-Type':
                   'application/json'}
        r = requests.put(url, cookies=self.cookies, data=json.dumps(data),
                         headers=headers, verify=False)
        return r

    def post(self, url, data):
        headers = {'Accept': 'text/plain, */*; q=0.01',
                   'Content-Type': 'application/json'}
        r = requests.post(url, cookies=self.cookies, data=json.dumps(data),
                          headers=headers, verify=False)
        return r

    def postXml(self, url, data):
        iheaders = {'Accept': 'text/plain, */*; q=0.01',
                   'Content-Type': 'application/xml'}
        r = requests.post(url, cookies=self.cookies, data=data,
                          headers=iheaders, verify=False)
        return r

    def delete(self, url):
        headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip,deflate,sdch'}
        r = requests.delete(url, cookies=self.cookies, headers=headers,
                            verify=False)


    def delete(self, url):
        headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip,deflate,sdch'}
        r = requests.delete(url, cookies=self.cookies, headers=headers,
                            verify=False)
        return r

    # get last job
    def last_job(self, did):
        """
        :param did:
        :return: jid
        """
        url = self.server + "/matelive/api/jobs"
        get_params = { 'size': 1,
                       'offset': 0,
                       'sortDir': 'dec',
                       'sortProp': 'jobId',
                       'filters': 'definitionId(' + did + ');'
        }
        r = self.get(url, get_params)
        jid = r.json()["jobList"][0]["jobId"]
        return jid

    # get csv data
    def get_csv_file(self, jid):
        get_params = {}
        get_params['nPerPage'] = 0
        url = self.server + "/matelive/services/reportout/" + str(jid)
        r = self.get(url, get_params)
        # get csv url
        csvurl = r.json()["table"]["csvUrl"]
        # get csv data
        url = self.server + "/matelive/" + csvurl
        r = self.get(url)
        return r.text


    def flush_myreports(self):
        url = self.server + "/matelive/api/myreports?size=1000&offset=0&sortDir=dec&sortProp=definitionId&filters="
        r = self.get(url)
        myreports = r.json()["myReportList"]

        for report in myreports:
            did = report["definitionId"]
            url = self.server + "/matelive/api/definitions/" + str(did)
            data = {'isMyReport': 'false'}
            r = self.put(url, data)
            # exit if error
            r.raise_for_status()
            print 'delete {:<50s} [{:s}]   {:s}'.\
                format(report["definitionName"], str(r.status_code), r.text)

    def flush_props(self):
        url = self.server + "/matelive/api/properties"
        r = self.get(url)
        props = r.json()["properties"]

        for prop in props:
            prop_name = prop["name"]
            url = self.server + "/matelive/api/properties/" + \
                str(prop["objectType"]) + "/" + str(prop_name)
            r = self.delete(url)
            # exit if error
            r.raise_for_status()
            print 'delete {:<50s} [{:s}]   {:s}'.\
                format(prop_name, str(r.status_code), r.text)

    def my_reports_list(self):
        url = self.server + "/matelive/api/myreports?size=1000&offset=0&\
            sortDir=dec&sortProp=definitionId&filters="
        r = self.get(url)
        myreports = r.json()["myReportList"]
        return myreports

    def my_reports_definitions(self):
        myreports = self.my_reports_list()
        array = []
        for report in myreports:
            did = report["definitionId"]
            url = self.server + "/matelive/api/definitions/" + str(did)
            r = self.get(url)
            array.append(r.json())
        return array

    def props(self):
        url = self.server + "/matelive/api/properties"
        r = self.get(url)
        r.raise_for_status()
        props = r.json()["properties"]
        return props

    def load_myreports_from_file(self, file):
        counter = 0
        success = 0
        # loop through the list of report definitions stored in the "reports"
        # file
        with open(file) as data_file:
            reports = json.load(data_file)
            for reportdef in reports:
                counter = counter + 1
                # create the report
                url = self.server + "/matelive/api/definitions/"
                r = self.post(url, reportdef)
                print '{:<3d} {:50s} [{:s}]   {:s}'.format(counter, reportdef["name"], str(r.status_code), r.text)
                url = self.server + "/matelive/api/definitions/" + \
                    str(reportdef["definitionId"])
                # set isMyReport to true in case the report existed
                if r.status_code == 201:
                    did = r.text
                    url = self.server + "/matelive/api/definitions/" + str(did)
                    data = {'isMyReport': 'true'}
                    r = self.put(url, data)
                    # exit if error
                    r.raise_for_status()
                    success = success + 1
            print "---"
            print str(success) + "/" + str(counter) + " loaded successfully."

    def load_props_from_file(self, file):
        counter = 0
        success = 0
        # loop through the list of report definitions stored in the "reports"
        # file
        with open(file) as data_file:
            props = json.load(data_file)
            for prop in props:
                counter = counter + 1
                # create the report
                url = self.server + "/matelive/api/properties/"
                r = self.post(url, prop)
                print '{:<3d} {:50s} [{:s}]   {:s}'.format(counter, prop["name"], str(r.status_code), r.text)
                if r.status_code == 201:
                    # exit if error
                    success = success + 1
        print "---"
        print str(success) + "/" + str(counter) + " loaded successfully."

    def run_report(self, did):
        url = self.server + "/matelive/runReport?&outputXml&bg&mid=" + str(did)
        r = self.get(url)
        root = ET.fromstring(r.text)
        jid = root.find("jid").text
        return jid

    def job_status(self, jid):
        url = self.server + "/matelive/reportStatus?jid=" + str(jid)
        r = self.get(url)
        root = ET.fromstring(r.text)
        status = root.find("status").text
        return status

    def scheduler_job_status(self, jid):
        url = self.server + "/matelive/services/scheduler/jobs/" + str(jid)
        r = self.get(url)
        dict = json.loads(r.text)
        status = dict['status']
        return status

    def explore(self, object_type, filter=None, count=10, properties=None, sort_prop=None, sort_dir='dec'):
        ''' Get the list of objects.'''
        get_params = {'size':         count,
                      'offset':       '0',
                      'hideInactive': 'true'
                      }
        if filter:
            get_params['filter'] = filter
        if sort_prop:
            get_params['sortProp'] = sort_prop
            get_params['sortDir'] = sort_dir

        url = self.server + "/matelive/api/objects/" + object_type
        r = self.get(url, get_params)
        l = MLTable()

        meta = r.json()['objectMeta']
        props_from_meta = []
        for p in meta:
            props_from_meta.append(p['name'])

        if not properties:
            properties = props_from_meta

        l['header'] = properties
        l['rows'] = []

        for line in r.json()['objectData']:
            row = []
            for prop in properties:
                row.append(line['data'][props_from_meta.index(prop)])
            l['rows'].append(row)
        return l

    def get_report_output_filter_sort(self, jid):
        get_params = {}
        get_params['nPerPage'] = 0
        url = self.server + "/matelive/services/reportout/" + str(jid)
        r = self.get(url,get_params)
        sorts_list = r.json().get('table').get('sorts')
        sorts = ""
        if sorts_list:
            for s in sorts_list:
                    sorts += str(s['colIndex'])+"("+ str(s['sortDir']) + ")"
        filters = r.json().get('table').get('filters')
        mymltable = self.get_report(jid,count=1000000,sorts=sorts,filters=filters)
        return {'sorts': sorts, 'filters': filters}

    def get_filtered_report(self, jid, columns=None, count=10):
        r = self.get_report_output_filter_sort(jid)
        return self.get_report(jid, columns, count, r.get('sorts'), r.get('filters'))

    def get_report(self, jid, columns=None, count=10, sorts=None, filters=None):
        url = self.server + "/matelive/services/reportout/" + str(jid)
        get_params = {}
        get_params['nPerPage'] = count
        # JG on 3/11/14: I guess this is a bug, it has to be set to ""
        get_params['filters'] = filters if filters is not None else ""
        get_params['sort'] = sorts if sorts is not None else ""

        r = self.get(url, get_params)
        res = MLTable()
        res['header'] = r.json()['table']['headers']
        res['rows'] = []
        for row in r.json()['table']['rows']:
            res['rows'].append(row)

        # triming to selected columns #
        if columns:
            tmp = []
            for i, v in enumerate(res['header']):
                if i in columns:
                    tmp.append(v)
            res['header'] = tmp
            rows = []
            for row in res['rows']:
                tmp = []
                for i, v in enumerate(row):
                    if i in columns:
                        tmp.append(v)
                rows.append(tmp)
            res['rows'] = rows
        return res

    def get_plan(self, date=None):
        from requests.auth import HTTPBasicAuth
        headers = {'Accept': 'application/json, text/javascript, */*'}
        get_params = {}
        if date:
            pattern = '%y%m%d_%H%M_%Z'
            epoch = int(calendar.timegm(time.strptime(date, pattern))) * 1000
            get_params['timestamp'] = str(epoch)
        url = self.server + "/map/api/archive/planfile"
        # Can't use self.get because the cookie-based auth doesn't seem to work
        r = requests.get(
            url, cookies=self.cookies, headers=headers, verify=False, params=get_params,
            auth=(self.credentials['username'], self.credentials['password']))
        try:
            r.raise_for_status()
        except Exception, e:
            print e
            print r.content
        timestamp = r.headers['x-filename']
        ret = {'timestamp': timestamp, 'file-content': r.content}
        return ret
        # print r.content

    def time_series(self, ob, prop, keys, date_from, date_to, keyColumns=None):
        keys_names = {}
        keys_names['Interfaces'] = ['Node', 'Name']
        keys_names['LSPs'] = ['SourceNode', 'Name']
        keys_names['Nodes'] = ['Node']

	if keyColumns!=None:
            keys_names[ob] = keyColumns

        keys_json = []
        for i, k in enumerate(keys):
            keys_json.append(
                {'name': keys_names[ob][i], 'value': keys[i]}
            )


        date_pattern = "%Y-%m-%d %H:%M:00"
        data = {'hasRawData': True,
                'isLive': True,
                'objectKeys': [{'keyPairs': keys_json}],
                'objectType': ob,
                'properties': [{
                    'aggregationMode': 'Last',
                    'name': prop
                }],
                'reportType': 'Adhoc',
                'timeFrom': time.strftime(date_pattern, date_from),
                'timeTo': time.strftime(date_pattern, date_to),
                }
        #        'timeRangeUnits': 'day',
        #        'timeRangeValue': '1'
        url = self.server + "/matelive/api/jobs/live"
        # should not be needed
        r = self.post(url, data)
        csvurl = r.json()['rors'][0]['propOuts'][0]['raw']['csvUrl']
        url = self.server + "/" + csvurl
        r = self.get(url)
        return r.text

    def traff_report(self, ob, date_from, date_to):
        '''
        in progress. doesn't work.
        '''
        keys_json = []
        data = {'hasRawData': True,
                'isLive': True,
                'objectKeys': [{'keyPairs': keys_json}],
                'objectType': ob,
                'reportType': 'Adhoc',
                'timeFrom': time.strftime(date_from),
                'timeTo': time.strftime(date_to),
                }
        url = self.server + "/matelive/api/jobs/live"
        r = self.post(url, data)
        csvurl = r.json()['rors'][0]['propOuts'][0]['raw']['csvUrl']
        url = self.server + "/" + csvurl
        r = self.get(url)
        return r.text

    def create_table(self, file):
        fh = open(file, "r+")
        data = fh.read()

        url = self.server + "/matelive/api/data/newtable/"
        if re.search('tableDefinition',data):
            # for xml format
            r = self.postXml(url, data)
        else:
	    data = json.loads(data)
            r = self.post(url, data)
        return r

    def import_data(self, table, file, timestamp):
        fh = open(file, "r+")
        data = fh.read()

        url = self.server + "/matelive/api/data/" + table + "?file=" + file + "&time=" + timestamp
        r = self.post(url, data)
        return r

    def drop_table(self, table):
        url = self.server + "/matelive/api/data/droptable/" + table
        r = self.delete(url)
        return r

def parse_url(url):
    parsed = urlparse(url)
    new_url = None
    if parsed.port:
        new_url = parsed.scheme + "://" + \
            str(parsed.hostname) + ":" + str(parsed.port)
    else:
        new_url = parsed.scheme + "://" + parsed.hostname
    return parsed.username, parsed.password, new_url


class MLTable (dict):
    '''
    handles list printing
    '''
    def print_col(self):
        '''
        display this:
            {header: [h1, h2], rows: [ [val1, val2], [val3, val4]]}
        like that:
        +-------+------+
        | h1    | h2   |
        +-------+------+
        | val1  | val2 |
        | val3  | val4 |
        +-------+------+
        '''
        max_len = OrderedDict()

        # determine max value length accross keys and rows values

        for v in self['header']:
            if isinstance(v, list):
                v = "<list of objects>"
            if v in max_len.keys():
                if len(str(v)) > max_len[v]:
                    max_len[v] = len(str(v)) + 1
            else:
                max_len[v] = len(str(v)) + 1

        max_len_list = list(max_len.values())
        for row in self['rows']:
            for i, v in enumerate(row):
                if isinstance(v, list):
                    v = "<list of objects>"
                if len(str(v)) > max_len_list[i]:
                    max_len_list[i] = len(str(v)) + 1

        # print border
        border = "+"
        for i, v in enumerate(self['header']):
            border = border + '{:s}{:s}'.format("-" * (max_len_list[i] + 2), "+")
        print border

        # print keys as headers
        header = "| "
        for i, v in enumerate(self['header']):
            strformat = '{:<' + str(max_len_list[i] + 1) + '}'
            header = header + strformat.format(v) + "| "
        print header

        # print border
        print border

        # print values
        for i, r in enumerate(self['rows']):
            row = "| "
            for i, v in enumerate(r):
                if isinstance(v, list):
                    v = "<list of objects>"
                strformat = '{:<' + str(max_len_list[i] + 1) + '}'
                row = row + strformat.format(v) + "| "
            print row

        # print border
        print border

    def print_csv(self):
        # print keys
        for cell in self['header']:
            print cell, "\t",
        print
        for row in self['rows']:
            for cell in row:
                print cell, "\t",
            print
        print
