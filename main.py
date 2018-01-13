#!/usr/bin/python
import sys
import os
import stashy
import pprint

username = ''
password = ''
stash = stashy.connect("stash", username, password)

projects = stash.projects.list()

# /Users//Documents/python/stash/delete
starting_dir = os.getcwd() + '/' + 'delete/'

# Projects
for project in projects:
    pprint.pprint('Folder Name: ' + project['name'])
    pprint.pprint('Project Key: ' + project['key'])
    project_key = project['key']

    projectsRepos = stash.projects[project_key].repos
    project_repositories = projectsRepos.list()

    # pprint.pprint(project_repositories)
    # print '\n'
    for repository in project_repositories:
        pprint.pprint('Project Name: ' + repository['name'])
        pprint.pprint('Git URL: ' + repository['links']['clone'][0]['href'])
        path = starting_dir + project['name'] +'/'+ repository['name']
        print path
        os.makedirs(path)
        os.chdir(path)
        os.system("git clone %s" % repository['links']['clone'][0]['href'])
        os.chdir(starting_dir)
        print '\n'