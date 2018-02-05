import os
import bitbucket
import settings
import pprint

bitbucket_username = os.environ.get("BITBUCKET_USERNAME")
bitbucket_password = os.environ.get("BITBUCKET_PASSWORD")
bitbucket_host     = os.environ.get("BITBUCKET_HOST")

bb = bitbucket.BitBucket(bitbucket_host, bitbucket_username, bitbucket_password)

# print("Create Project AKA: Client \n")
# response1 = bb.createProject('TEST', 'Testing Project3e', 'Just another testing')
# pprint.pprint(response1)
# print("\n")

print("response4 \n")
response4 = bb.setProjectPermissions('TEST', 'groups', 'administrators', 'admin')
pprint.pprint(response4)
print("\n")

print("response4 \n")
response4 = bb.setProjectPermissions('TEST', 'users', 'Ethan.Desilets', 'admin')
pprint.pprint(response4)
print("\n")

# print("Create a repository in a project AKA: Client \n")
# response2 = bb.createProjectRepository('TEST', 'site mover')
# pprint.pprint("Slug shouldn't be NONE")
# pprint.pprint(response2)
# print("\n")

repositorySlug = "site-mover"

# print("Set Repository Permission: User \n")
# response3 = bb.setRepositoryPermissions('TEST', repositorySlug, "users", 'Ethan.Desilets', 'admin')
# pprint.pprint(response3)
# print("\n")

# print("Set Repository Permission: Group \n")
# response3a = bb.setRepositoryPermissions('TEST', repositorySlug, "groups", 'Administrators', 'admin')
# pprint.pprint(response3a)
# print("\n")

# print("git push origin --all")

# if response.get("errors"):
#     print("Push error to dict\n");
# else:
#     print("moving on\n");
