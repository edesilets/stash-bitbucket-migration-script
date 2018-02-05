import os
import bitbucket
import stash
import settings
import pprint

bitbucket_username = os.environ.get("BITBUCKET_USERNAME")
bitbucket_password = os.environ.get("BITBUCKET_PASSWORD")
bitbucket_host     = os.environ.get("BITBUCKET_HOST")

stash_username = os.environ.get("STASH_USERNAME")
stash_password = os.environ.get("STASH_PASSWORD")
stash_host     = os.environ.get("STASH_HOST")

# bb = bitbucket.BitBucket(bitbucket_host, bitbucket_username, bitbucket_password)

# print("Create Project AKA: Client \n")
# response1 = bb.createProject('TEST', 'Testing Project3e', 'Just another testing')
# pprint.pprint(response1)
# print("\n")

# print("response4 \n")
# response4 = bb.setProjectPermissions('TEST', 'groups', 'administrators', 'admin')
# pprint.pprint(response4)
# print("\n")

# print("response4 \n")
# response4 = bb.setProjectPermissions('TEST', 'users', 'Ethan.Desilets', 'admin')
# pprint.pprint(response4)
# print("\n")

# print("Create a repository in a project AKA: Client \n")
# response2 = bb.createProjectRepository('TEST', 'site mover')
# pprint.pprint("Slug shouldn't be NONE")
# pprint.pprint(response2)
# print("\n")

# repositorySlug = response2.get('slug')

# print("Set Repository Permission: User \n")
# response3 = bb.setRepositoryPermissions('TEST', repositorySlug, "users", 'Ethan.Desilets', 'admin')
# pprint.pprint(response3)
# print("\n")

# print("Set Repository Permission: Group \n")
# response3a = bb.setRepositoryPermissions('TEST', repositorySlug, "groups", 'Administrators', 'admin')
# pprint.pprint(response3a)
# print("\n")

# print("git push origin --all")

stash = stash.Stash(stash_host, stash_username, stash_password)
projects = stash.getProjects()

# /Users/userName/Documents/python/stash/delete
starting_dir = os.getcwd() + '/' + 'delete/'

# Projects
for project in projects:
    pprint.pprint('Folder Name: ' + project['name'])
    pprint.pprint('Project Key: ' + project['key'])
    project_key = project['key']

    projectsRepos = stash.getProjectRepositories(project_key)
    project_repositories = projectsRepos.list()

    # pprint.pprint(project_repositories)
    # print '\n'
    for repository in project_repositories:
        pprint.pprint('Project Name: ' + repository['name'])
        pprint.pprint('Git URL: ' + repository['links']['clone'][0]['href'])
        path = starting_dir + project['name'] +'/'+ repository['name']
        print path
        # os.makedirs(path)
        # os.chdir(path)
        # os.system("git clone %s" % repository['links']['clone'][0]['href'])
        # os.chdir(starting_dir)
        print '\n'
