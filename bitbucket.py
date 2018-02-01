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

class BitBucketRequest:
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

    def clearPayload(self):
        self.payload = dict()

    def send(self, method, uri):
        encodedpayload = json.dumps(self.payload);

        # encode playload and headers and send request to server BB test....
        response = requests.request(method, self.baseurl+uri, data=encodedpayload, headers=self.headers, verify=False)
        decoded = json.loads(response.text)
        return decoded

class BitBucket(BitBucketRequest):
    def __init__(self, host, username, password):
        self.bitBucketRequest = BitBucketRequest(host, username, password)

    def createRepository(self, key, name, description):
        self.bitBucketRequest.setPayload("key", key)
        self.bitBucketRequest.setPayload("name", name)
        self.bitBucketRequest.setPayload("description", description)
        response = self.bitBucketRequest.send("POST", "projects")
        self.bitBucketRequest.clearPayload()
        return response

bb = BitBucket(host, username, password)
response = bb.createRepository('PRJ', 'Testing Project3', 'Just another testing')
pprint.pprint(response)