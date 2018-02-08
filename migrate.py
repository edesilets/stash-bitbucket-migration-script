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
bitbucket_ssh_key_path = os.environ.get("BITBUCKET_SSH_KEY_PATH")

stash_username = os.environ.get("STASH_USERNAME")
stash_password = os.environ.get("STASH_PASSWORD")
stash_host     = os.environ.get("STASH_HOST")
stash_ssh_key_path = os.environ.get("STASH_SSH_KEY_PATH")

class Migrate(bitbucket.BitBucket,stash.Stash):
    def __init__(self):
        self.bb = bitbucket.BitBucket(bitbucket_host, bitbucket_username, bitbucket_password)
        self.stash = stash.Stash(stash_host, stash_username, stash_password)
        self.stashProjects = self.stash.getProjects()

    def gitSSHCommand(self, ssh_key_path):
        git_ssh_identity_file = os.path.expanduser(ssh_key_path)
        git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
        pprint.pprint("Git using ssh comand: "+git_ssh_cmd)
        return git_ssh_cmd

    def gitUrlParse(self, url, ssh_conf_name):
        urlParsed = urlparse(url)
        modify = url.replace(urlParsed.netloc, ssh_conf_name)
        return modify

    def findGitSSHURL(self, clone_url_array):
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
    def setupBitBucketProject(self, projectkey, projectName):
        self.bb.createProject(projectkey, projectName, '')
        self.bb.setProjectPermissions(projectkey, "group", "Administrators", 'admin')
        self.bb.setProjectPermissions(projectkey, "user", "Ethan.Desilets", 'admin')

    def setupBitBucketRepository(self, projectKey, name):
        repositoryInfo = self.bb.createProjectRepository(projectKey, name)
        repositoryKey  = repositoryInfo['slug']
        repositoryCloneUrls = repositoryInfo['links']['clone']
        repositoryGitUrl = self.findGitSSHURL(repositoryCloneUrls)

        self.bb.setRepositoryPermissions(projectKey, repositoryKey, "group", "Administrators", 'admin')
        self.bb.setRepositoryPermissions(projectKey, repositoryKey, "user", "Ethan.Desilets", 'admin')
        return repositoryGitUrl

    ##### Extraction Process
    def cloneFromStash(self, git_clone_url, clone_to_dir):
        git_ssh_cmd = self.gitSSHCommand(stash_ssh_key_path)
        Repo.clone_from(git_clone_url, clone_to_dir,env={'GIT_SSH_COMMAND': git_ssh_cmd })
        pprint.pprint("Clone from STASH completed")

        pprint.pprint("Fetching from STASH")
        Repo(clone_to_dir).remote(name='origin').fetch()
        pprint.pprint("Fetching from STASH completed")

    def uploadToBitBucket(self, git_remote_url, git_folder_path):
            git_folder_path = os.path.normpath(git_folder_path)
            # Add new bitbucket remote
            cleanURL = self.gitUrlParse(git_remote_url, 'bitBucketGit')
            Repo(git_folder_path).create_remote('bitbucket', url=cleanURL)

            pprint.pprint("Bitbucket Git URL: "+cleanURL)
            git_ssh_cmd = self.gitSSHCommand(bitbucket_ssh_key_path)
            with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
                pprint.pprint("Pushing Branches to BitBucket")
                # refs/remotes/origin/*:refs/heads/*    VERY close but pushes HEAD in bitbucket.....
                Repo(git_folder_path).remote(name='bitbucket').push(refspec="+refs/remotes/origin/*:refs/heads/*")
                pprint.pprint("Pushing Branches to BitBucket COMPLETE")
                pprint.pprint("Pushing Tags to BitBucket")
                Repo(git_folder_path).remote(name='bitbucket').push(refspec="+refs/tags/*:refs/tags/*")
                pprint.pprint("Pushing Tags to BitBucket COMPLETE")

                # NOTE: refspec=":HEAD" Deletes the HEAD branch that is created on the new remote AKA: bitbucket
                pprint.pprint("Delete HEAD bransh on BitBucket")
                Repo(git_folder_path).remote(name='bitbucket').push(refspec=":HEAD")
                pprint.pprint("Delete HEAD bransh on BitBucket COMPLETE!")
            print "Pushing to BitBucket completed"

    def setupRepositoryDirectory(self, project_name, repository_name):
        # /Users/userName/Documents/python/stash/export
        clone_path = os.getcwd() + '/export/' + project_name + "/" + repository_name
        clone_path_normalize = os.path.normpath(clone_path)
        if not os.path.exists(clone_path_normalize):
            os.makedirs(clone_path_normalize)
        return clone_path_normalize
