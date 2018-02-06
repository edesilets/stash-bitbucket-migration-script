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

##### Utilities 
def gitUrlParse(url, ssh_conf_name):
    urlParsed = urlparse(url)
    modify = url.replace(urlParsed.netloc, ssh_conf_name)
    return modify

def findGitSSHURL(clone_url_array):
    error_message = "Could not find Git ssh url in clone array!"
    if clone_url_array:
        for urlDescription in clone_url_array:
            if urlDescription.has_key("name") and urlDescription.has_key("href"):
                if urlDescription["name"] == "ssh":
                    return urlDescription["href"]
            else:
                sys.exit(error_message)
    else:
        sys.exit(error_message)

##### Setup Process
def setupBitBucketProject(projectkey, projectName):
    bb.createProject(projectkey, projectName, '')
    bb.setProjectPermissions(projectkey, "group", "Administrators", 'admin')
    bb.setProjectPermissions(projectkey, "user", "Ethan.Desilets", 'admin')

def setupBitBucketRepository(projectKey, name):
    repositoryInfo = bb.createProjectRepository(projectKey, name)
    repositoryKey  = repositoryInfo['slug']
    repositoryCloneUrls = repositoryInfo['links']['clone']
    repositoryGitUrl = findGitSSHURL(repositoryCloneUrls)

    bb.setRepositoryPermissions(projectKey, repositoryKey, "group", "Administrators", 'admin')
    bb.setRepositoryPermissions(projectKey, repositoryKey, "user", "Ethan.Desilets", 'admin')
    return repositoryGitUrl

##### Extraction Process
def cloneFromStash(git_clone_url, clone_to_dir):
    git_ssh_identity_file = os.path.expanduser('~/.ssh/ethanDstash')
    git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
    pprint.pprint("Clone from STASH with command: "+ git_ssh_cmd)
    Repo.clone_from(git_clone_url, clone_to_dir,env={'GIT_SSH_COMMAND': git_ssh_cmd })
    pprint.pprint("Clone from STASH completed")

def uploadToBitBucket(git_remote_url, git_folder_path):
        git_folder_path = os.path.normpath(git_folder_path)
        # Add new bitbucket remote
        cleanURL = gitUrlParse(git_remote_url, 'bitBucketGit')
        Repo(git_folder_path).create_remote('bitbucket', url=cleanURL)

        git_ssh_identity_file = os.path.expanduser('~/.ssh/bitBucket')
        git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file

        pprint.pprint("Bitbucket Git URL: "+git_folder_path)
        pprint.pprint("Pushing to bitBucket with command: "+git_ssh_cmd)
        with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
            Repo(git_folder_path).remote(name='bitbucket').push('master')
        pprint.pprint("Pushing to bitbucket completed")

        # repo   = Repo(gitFolderPath)
        # ssh_cmd = 'ssh -i /Users/ethan.desilets/.ssh/bitBucket'
        # with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
        #     # repo.remotes.origin.fetch()
        #     repo.remote(name='bitbucket').push()

def setupRepositoryDirectory(project_name, repository_name):
    # /Users/userName/Documents/python/stash/export
    clone_path = os.getcwd() + '/export/' + project['name'] + "/" + repository['name']
    clone_path_normalize = os.path.normpath(clone_path)
    if not os.path.exists(clone_path_normalize):
        os.makedirs(clone_path_normalize)
    return clone_path_normalize


bb       = bitbucket.BitBucket(bitbucket_host, bitbucket_username, bitbucket_password)
stash    = stash.Stash(stash_host, stash_username, stash_password)
projects = stash.getProjects()

# Projects
for project in projects:
    pprint.pprint('Stash Folder Name: ' + project['name'])
    pprint.pprint('Stash Project Key: ' + project['key'])
    print "\n"
    project_key = project['key']

    projectsRepos = stash.getProjectRepositories(project_key)
    project_repositories = projectsRepos.list()

    setupBitBucketProject(project_key, project['name'])

    for repository in project_repositories:
        stash_git_url = findGitSSHURL(repository['links']['clone'])
        repository_name = repository['name']

        pprint.pprint('Stash Project Name: ' + repository_name)
        bitBucketGitUrl = setupBitBucketRepository(project_key, repository_name)

        clone_to_path = setupRepositoryDirectory(project['name'], repository_name)
        pprint.pprint("Generated Local Path: " + clone_to_path)
        pprint.pprint('Stash Git URL: ' + stash_git_url)

        print "\n"
        cloneFromStash(stash_git_url, clone_to_path)
        print "\n"
        uploadToBitBucket(bitBucketGitUrl, clone_to_path)
        print "\n"
        pprint.pprint("Directory after getting ready for next clone:  " + os.getcwd())
        print "########### Moving to next REPOSITORY! ###########\n\n\n"
    break
