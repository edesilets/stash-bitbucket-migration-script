import os
import bitbucket
import stash
import settings
import pprint
from urlparse import urlparse
from git import Repo
from git import Git

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

def setupBitBucketProject(projectkey, projectName):
    bb.createProject(projectkey, projectName, '')
    bb.setProjectPermissions(projectkey, "group", "Administrators", 'admin')
    bb.setProjectPermissions(projectkey, "user", "Ethan.Desilets", 'admin')

def setupBitBucketRepository(projectKey, name):
    repositoryInfo = bb.createProjectRepository(projectKey, name)
    repositoryKey  = repositoryInfo['slug']
    repositoryGitUrl = repositoryInfo['links']['clone'][0]['href']

    bb.setRepositoryPermissions(projectKey, repositoryKey, "group", "Administrators", 'admin')
    bb.setRepositoryPermissions(projectKey, repositoryKey, "user", "Ethan.Desilets", 'admin')
    return repositoryGitUrl

def uploadToBitBucket(git_remote_url, git_folder_path):
        cleanURL = gitUrlParse(git_remote_url, 'bitBucketGit')
        add_remote = "git remote add bitbucket %s" % cleanURL
        pprint.pprint(add_remote)
        os.system(add_remote)
        os.system("git fetch origin")

        git_ssh_identity_file = os.path.expanduser('~/.ssh/bitBucket')
        git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
        pprint.pprint(git_ssh_cmd)
        with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
            pprint.pprint("Pushing to bitBucket!!!")
            Repo(git_folder_path).remote(name='bitbucket').push('master')
            pprint.pprint("Pushing to COMPLETE!!!")

        # repo   = Repo(gitFolderPath)
        # ssh_cmd = 'ssh -i /Users/ethan.desilets/.ssh/bitBucket'
        # with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
        #     # repo.remotes.origin.fetch()
        #     repo.remote(name='bitbucket').push()

def saveRepositoriesLocally(repository, project, bitBucketGitUrl):
        stash_git_url = repository['links']['clone'][0]['href']
        pprint.pprint('Stash Git URL: ' + stash_git_url)

        path = starting_dir + project['name']

        if not os.path.exists(path):
            os.makedirs(path)

        pprint.pprint("Local Path: " + path)
        os.chdir(path)

        os.system("git clone %s" % stash_git_url)

        # hyphens and lower case missing from repo name to git clone folder name
        gitFolderPath = path+"/"+repository['name'].lower().replace(" ","-")

        os.chdir(gitFolderPath)
        pprint.pprint("Directory after clone:  " +os.getcwd())

        uploadToBitBucket(bitBucketGitUrl, gitFolderPath)

        os.chdir(starting_dir)
        pprint.pprint("Directory after getting ready for next clone:  " +os.getcwd())
        print '\n'

bb       = bitbucket.BitBucket(bitbucket_host, bitbucket_username, bitbucket_password)
stash    = stash.Stash(stash_host, stash_username, stash_password)
projects = stash.getProjects()

# /Users/userName/Documents/python/stash/export
starting_dir = os.getcwd() + '/' + 'export/'

# Projects
for project in projects:
    pprint.pprint('Stash Folder Name: ' + project['name'])
    pprint.pprint('Stash Project Key: ' + project['key'])
    project_key = project['key']

    projectsRepos = stash.getProjectRepositories(project_key)
    project_repositories = projectsRepos.list()

    # pprint.pprint(project_repositories)
    # print '\n'
    setupBitBucketProject(project_key, project['name'])

    for repository in project_repositories:
        pprint.pprint('Stash Project Name: ' + repository['name'])
        bitBucketGitUrl = setupBitBucketRepository(project_key, repository['name'])
        saveRepositoriesLocally(repository, project, bitBucketGitUrl)

        print "########### Moving to next REPOSITORY! ###########\n\n\n\n\n"
    break
