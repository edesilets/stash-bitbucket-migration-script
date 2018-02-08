import os
import migrate
import pprint
import time

Migrate = migrate.Migrate()

# Projects
for project in Migrate.stashProjects:
    project_time_start = time.time()
    print "########### Exporting Project "+project['name']+" ###########"
    pprint.pprint('Stash Folder Name: ' + project['name'])
    pprint.pprint('Stash Project Key: ' + project['key'])
    print "\n"
    project_key = project['key']

    projectsRepos = Migrate.stash.getProjectRepositories(project_key)
    project_repositories = projectsRepos.list()

    Migrate.setupBitBucketProject(project_key, project['name'])

    for repository in project_repositories:
        repository_time_start = time.time()

        print "########### Migrating "+repository['name']+" from STASH! ###########"
        stash_git_url = Migrate.findGitSSHURL(repository['links']['clone'])
        repository_name = repository['name']

        bitBucketGitUrl = Migrate.setupBitBucketRepository(project_key, repository_name)
        clone_to_path   = Migrate.setupRepositoryDirectory(project['name'], repository_name)

        pprint.pprint("Generated Local Path: " + clone_to_path)
        pprint.pprint('Stash Git URL: ' + stash_git_url)

        print "\n"
        Migrate.cloneFromStash(stash_git_url, clone_to_path)
        print "\n"
        Migrate.uploadToBitBucket(bitBucketGitUrl, clone_to_path)
        repository_time_end = time.time()
        print("--- Repository Migration took %s seconds ---" % (repository_time_end - repository_time_start))
        print "########### Moving to next REPOSITORY! ###########\n\n"

    project_time_end = time.time()
    print("--- Project Migration took %s seconds ---" % (project_time_end - project_time_start))
    print "########### Completed Export of Project "+project['name']+" ###########"
    break
