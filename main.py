import os
import bitbucket
import stash
import settings
import pprint
from urlparse import urlparse

bitbucket_username = os.environ.get("BITBUCKET_USERNAME")
bitbucket_password = os.environ.get("BITBUCKET_PASSWORD")
bitbucket_host     = os.environ.get("BITBUCKET_HOST")

stash_username = os.environ.get("STASH_USERNAME")
stash_password = os.environ.get("STASH_PASSWORD")
stash_host     = os.environ.get("STASH_HOST")

def gitUrlParse(url, ssh_conf_name):
    urlParsed = urlparse(url)
    modify = url.replace(urlParsed.netloc, ssh_conf_name)
    return modify

def saveRepositoriesLocally(repository, project):
        pprint.pprint('Project Name: ' + repository['name'])
        pprint.pprint('Git URL: ' + repository['links']['clone'][0]['href'])
        path = starting_dir + project['name'] +'/'+ repository['name']
        print path
        # os.makedirs(path)
        # os.chdir(path)
        # os.system("git clone %s" % repository['links']['clone'][0]['href'])
        # os.chdir(starting_dir)
        print '\n'

stash    = stash.Stash(stash_host, stash_username, stash_password)
projects = stash.getProjects()

# /Users/userName/Documents/python/stash/export
starting_dir = os.getcwd() + '/' + 'export/'

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
        saveRepositoriesLocally(repository, project)
