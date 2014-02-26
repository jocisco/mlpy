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
#


import requests, json
import xml.etree.ElementTree as ET

class ML:
    def __init__ (self, server, credentials):
        self.credentials = credentials
        self.server = server
        self.cookies=self.login(credentials)

    def login(self, credentials):
        r = requests.post(self.server + "/matelive/services/auth/login", data=credentials, verify=False)
        r.raise_for_status()
        self.cookies = r.cookies
        return self.cookies

    def get (self, url):
        headers = {'Accept' : 'application/json, text/javascript, */*'} 
        r = requests.get(url, cookies=self.cookies, headers=headers, verify=False)
        return r

    def put(self,url,data):
        headers = {'Accept' : 'text/plain, */*; q=0.01', 'Content-Type' : 'application/json'} 
        r = requests.put(url, cookies=self.cookies, data=json.dumps(data), headers=headers, verify=False)
        return r
    
    def post(self,url,data):
        headers = {'Accept' : 'text/plain, */*; q=0.01', 'Content-Type' : 'application/json'} 
        r = requests.post(url, cookies=self.cookies, data=data, headers=headers, verify=False)
        return r

    def delete(self,url):
        headers = {'Accept' : '*/*', 'Accept-Encoding' : 'gzip,deflate,sdch'} 
        r = requests.delete(url, cookies=self.cookies, headers=headers, verify=False)
        return r

    # get last job
    def get_last_job(self, did):
        url = self.server + "/matelive/api/jobs?size=1&offset=0&sortDir=dec&sortProp=jobId&filters=definitionId("+did+")%3B"
        r = self.get(url)
        jid = r.json["jobList"][0]["jobId"]
        return jid

    # get csv data
    def get_csv(self,jid):
        # get csv url
        url = self.server + "/matelive/services/reportout/" + str(jid)
        r = self.get(url)
        csvurl = r.json["table"]["csvUrl"]
        # get csv data
        url = self.server + "/matelive/" + csvurl
        r = self.get(url)
        return r.text
    
    # get last csv data
    def get_last_csv(self,did):
        return self.get_csv(self.get_last_job(did))

    def clear_myreports(self):
        url = self.server + "/matelive/api/myreports?size=1000&offset=0&sortDir=dec&sortProp=definitionId&filters="
        r = self.get(url)
        myreports =  r.json["myReportList"]

        for report in myreports:
            did = report["definitionId"]
            url = self.server + "/matelive/api/definitions/" + str(did)
            data = {'isMyReport': 'false'}
            r = self.put(url,data)
            # exit if error
            r.raise_for_status()
            print 'delete {:<50s} [{:s}]   {:s}'.format(report["definitionName"], str(r.status_code), r.text)

    def clear_props(self):
        url = self.server + "/matelive/api/properties"
        r = self.get(url)
        props =  r.json["properties"]

        for prop in props:
            prop_name = prop["name"]
            url = self.server + "/matelive/api/properties/" + str(prop["objectType"]) + "/" + str(prop_name)
            r = self.delete(url)
            # exit if error
            r.raise_for_status()
            print 'delete {:<50s} [{:s}]   {:s}'.format(prop_name, str(r.status_code), r.text)       

    def my_reports(self):
        url = self.server + "/matelive/api/myreports?size=1000&offset=0&sortDir=dec&sortProp=definitionId&filters="
        r = self.get(url)
        myreports =  r.json["myReportList"]
        return myreports

    def my_reports_definitions(self):
        myreports=self.my_reports()
        array = []
        for report in myreports:
            did = report["definitionId"]
            url = self.server + "/matelive/api/definitions/" + str(did)
            r = self.get(url)
            array.append(r.json)
        return array

    def props(self):
        url = self.server + "/matelive/api/properties"
        r = self.get(url)
        r.raise_for_status()
        #props =  r.text["properties"]
        props =  r.json["properties"]
        return props

    def load_myreports_from_file(self,file):
        counter = 0
        success = 0
        # loop through the list of report definitions stored in the "reports" file
        with open(file) as data_file:    
            reports = json.load(data_file)
            for reportdef in reports:
                counter=counter+1
                # create the report
                url = self.server + "/matelive/api/definitions/"
                data=json.dumps(reportdef)
                r = self.post(url,data)
                print '{:<3d} {:50s} [{:s}]   {:s}'.format(counter, reportdef["name"], str(r.status_code), r.text)
                url = self.server + "/matelive/api/definitions/" + str(reportdef["definitionId"])
                # set isMyReport to true in case the report existed
                if r.status_code == 201:
                    did=r.text
                    url = self.server + "/matelive/api/definitions/" + str(did)
                    data = {'isMyReport': 'true'}
                    r = self.put(url,data)
                    # exit if error
                    r.raise_for_status()
                    success = success + 1
            print "---"
            print str(success) + "/" + str(counter) + " loaded successfully."

    def load_props_from_file(self,file):
        counter = 0
        success = 0
        # loop through the list of report definitions stored in the "reports" file
        with open(file) as data_file:    
            props = json.load(data_file)
            for prop in props:
                counter=counter+1
                # create the report
                url = self.server + "/matelive/api/properties/"
                data=json.dumps(prop)
                r = self.post(url,data)
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

    def get_job_status(self, jid):
        url = self.server + "/matelive/reportStatus?jid=" + str(jid)
        r = self.get(url)
        root = ET.fromstring(r.text)
        status = root.find("status").text
        return status
