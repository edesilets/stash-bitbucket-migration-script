import os
import migrate
import pprint

Migrate = migrate.Migrate()

# Projects
for project in Migrate.stashProjects:
    pprint.pprint('Stash Folder Name: ' + project['name'])
    pprint.pprint('Stash Project Key: ' + project['key'])
    print "\n"
    project_key = project['key']

    projectsRepos = Migrate.stash.getProjectRepositories(project_key)
    project_repositories = projectsRepos.list()

    Migrate.setupBitBucketProject(project_key, project['name'])

    for repository in project_repositories:
        stash_git_url = Migrate.findGitSSHURL(repository['links']['clone'])
        repository_name = repository['name']

        pprint.pprint('Stash Project Name: ' + repository_name)
        bitBucketGitUrl = Migrate.setupBitBucketRepository(project_key, repository_name)

        clone_to_path = Migrate.setupRepositoryDirectory(project['name'], repository_name)
        pprint.pprint("Generated Local Path: " + clone_to_path)
        pprint.pprint('Stash Git URL: ' + stash_git_url)

        print "\n"
        Migrate.cloneFromStash(stash_git_url, clone_to_path)
        print "\n"
        Migrate.uploadToBitBucket(bitBucketGitUrl, clone_to_path)
        print "\n"
        pprint.pprint("Directory after getting ready for next clone:  " + os.getcwd())
        print "########### Moving to next REPOSITORY! ###########\n\n\n"
        break
    break
