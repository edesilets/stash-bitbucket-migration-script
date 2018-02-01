#!/usr/bin/python
import sys
import os
import pprint
import requests
import json
import base64

username = ''
password = ''
host     = 'host'

class BitBucket:
    baseurl = ""
    headers = dict()
    payload = dict()

    def __init__(self, host, username, password):
        self.headers['Content-Type'] = "application/json"
        self.headers['Cache-Control'] = "no-cache"
        self.createConnection(host, username, password);

    def setHost(self, host):
        self.baseurl = "https://" + host + "/rest/api/1.0/"

    def setUser(self, username, password):
        self.headers['Authorization'] = "Basic " + base64.b64encode(username + ':' + password)

    def createConnection(self, host, username, password):
        self.setHost(host)
        self.setUser(username, password)

    def setPayload(self, param, value):
        self.payload[param] = value

    def send(self, method, uri):
        encodedpayload = json.dumps(self.payload);
        pprint.pprint(encodedpayload)
        # encode playload and headers and send request to server BB test....
        response = requests.request(method, self.baseurl+uri, data=encodedpayload, headers=self.headers, verify=False)
        decoded = json.loads(response.text)
        return decoded

    def test(self):
        return [self.baseurl , self.headers, self.payload]


bb = BitBucket(host, username, password)
bb.setPayload('description', 'Just another testing')
bb.setPayload('key', 'PRJ')
bb.setPayload("name", 'Testing Project3')
pprint.pprint(bb.test())
print("\n")
bb.send("POST", "projects")