#!/usr/bin/python
import sys
import os
import requests
import json
import base64
import pprint
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
        self.clearPayload()

        if response.ok and response.text:
            decoded = json.loads(response.text)
        else:
            decoded = response.text
        return decoded

class BitBucket(BitBucketRequest):
    def __init__(self, host, username, password):
        self.bitBucketRequest = BitBucketRequest(host, username, password)

    def createProject(self, key, name, description):
        self.bitBucketRequest.setPayload("key", key)
        self.bitBucketRequest.setPayload("name", name)
        self.bitBucketRequest.setPayload("description", description)
        response = self.bitBucketRequest.send("POST", "projects")
        return response

    def createProjectRepository(self, projectKey, name, forkable=True):
        self.bitBucketRequest.setPayload("name", name)
        self.bitBucketRequest.setPayload("scmId", "git")
        self.bitBucketRequest.setPayload("forkable", forkable)
        response = self.bitBucketRequest.send("POST", "projects/"+projectKey+"/repos")
        return response

    def setProjectPermissions(self, projectKey, user_or_group, name, permission):
        user_or_group = user_or_group.lower()
        if user_or_group == "group" or user_or_group == "groups":
            properUserGroup = "groups"
        elif user_or_group == "user" or user_or_group == "users":
            properUserGroup = "users"

        permission = permission.lower()
        if permission == "read":
            properPermission = "PROJECT_READ"
        elif permission == "write":
            properPermission = "PROJECT_WRITE"
        elif permission == "admin":
            properPermission = "PROJECT_ADMIN"

        uri            = "projects/"+projectKey+"/permissions/"+properUserGroup
        queryParams    = "?permission="+properPermission+"&name="+name
        fullyFormedURI = uri + queryParams
        response = self.bitBucketRequest.send("PUT", fullyFormedURI)
        return response

    def setRepositoryPermissions(self, projectKey, repository, user_or_group, name, permission):
        user_or_group = user_or_group.lower()
        if user_or_group == "group" or user_or_group == "groups":
            properUserGroup = "groups"
        elif user_or_group == "user" or user_or_group == "users":
            properUserGroup = "users"

        permission = permission.lower()
        if permission == "read":
            properPermission = "REPO_READ"
        elif permission == "write":
            properPermission = "REPO_WRITE"
        elif permission == "admin":
            properPermission = "REPO_ADMIN"

        uri            = "projects/"+projectKey+"/repos/"+repository+"/permissions/"+properUserGroup
        queryParams    = "?name="+name+"&permission="+properPermission
        fullyFormedURI = uri + queryParams

        response = self.bitBucketRequest.send("PUT", fullyFormedURI)
        return response
class BitBucket(BitBucketServer, BitBucketCloud):

    def __init__(self, host, username, password, cloud=False):
        if cloud:
            self.bitbucket = BitBucketCloud(host, username, password)
        else:
            self.bitbucket =  BitBucketServer(host, username, password)
