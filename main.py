import bitbucket
import settings

bitbucket_username = os.environ.get("BITBUCKET_USERNAME")
bitbucket_password = os.environ.get("BITBUCKET_PASSWORD")
bitbucket_host     = os.environ.get("HOST_BITBUCKET")

bb = BitBucket(bitbucketHost, username, password)

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