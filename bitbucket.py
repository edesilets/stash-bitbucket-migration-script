#!/usr/bin/python
import sys
import os
import pprint
import requests
import json
import base64
import settings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
host     = os.environ.get("HOST")

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

    def setProjectGroupPermissions(self, projectKey, name, permission):
        permission = permission.lower()
        if permission == "read":
            properPermission = "PROJECT_READ"
        elif permission == "write":
            properPermission = "PROJECT_WRITE"
        elif permission == "admin":
            properPermission = "PROJECT_ADMIN"

        uri            = "projects/"+projectKey+"/permissions/groups"
        queryParams    = "?permission="+properPermission+"&name="+name
        fullyFormedURI = uri + queryParams
        response = self.bitBucketRequest.send("PUT", fullyFormedURI)
        return response

    def setRepositoryUserPermissions(self, projectKey, repository, userName, permission):
        permission = permission.lower()
        if permission == "read":
            properPermission = "REPO_READ"
        elif permission == "write":
            properPermission = "REPO_WRITE"
        elif permission == "admin":
            properPermission = "REPO_ADMIN"

        uri            = "projects/"+projectKey+"/repos/"+repository+"/permissions/users"
        queryParams    = "?name="+userName+"&permission="+properPermission
        fullyFormedURI = uri + queryParams

        response = self.bitBucketRequest.send("PUT", fullyFormedURI)
        return response

bb = BitBucket(host, username, password)

# print("Create Project AKA: Client \n")
# response1 = bb.createProject('TEST', 'Testing Project3e', 'Just another testing')
# pprint.pprint(response1)
# print("\n")

# print("Create a repository in a project AKA: Client \n")
# response2 = bb.createProjectRepository('TEST', 'site mover')
# pprint.pprint("Slug shouldn't be NONE")
# pprint.pprint(response2.get("slug"))
# print("\n")

repositorySlug = "site-mover"

# print("Set Repository Permission: User \n")
# response3 = bb.setRepositoryUserPermissions('TEST', repositorySlug, 'Ethan.Desilets', 'admin')
# pprint.pprint(response3)
# print("\n")

print("Set Repository Permission: Group \n")
response3a = bb.setRepositoryPermissions('TEST', repositorySlug, "group", 'Administrators', 'admin')
pprint.pprint(response3a)
print("\n")

# print("response4 \n")
# response4 = bb.setProjectGroupPermissions('TEST', 'administrators', 'admin')
# pprint.pprint(response4)
# print("\n")

# print("git push origin --all")

# if response.get("errors"):
#     print("Push error to dict\n");
# else:
#     print("moving on\n");

# 3:14 pm
