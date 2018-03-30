import os
import migrate
import pprint
import time
import namingConventions

Migrate = migrate.Migrate()
stashInformation = Migrate.stashInformation

update_naming_convention = True

if update_naming_convention:
    stashInformation = namingConventions.NamingConventions().newInformation(stashInformation)

for project_key, project in stashInformation.iteritems():
    project_time_start = time.time()
    print '########### Exporting Project "'+project['name']+'" ###########'
    Migrate.setupBitBucketProject(project_key, project['name'])

    for repository in project['repositories']:
        repository_time_start = time.time()

        print '########### Migrating "'+repository['name']+'" from STASH! ###########'
        bitBucketGitUrl = Migrate.setupBitBucketRepository(project_key, repository['name'])
        clone_to_path   = Migrate.setupRepositoryDirectory(project['name'], repository['name'])

        pprint.pprint("Generated Local Path: " + clone_to_path)
        pprint.pprint('Stash Git URL: ' + repository['clone_url'])

        Migrate.cloneFromStash(repository['clone_url'], clone_to_path)
        Migrate.uploadToBitBucket(bitBucketGitUrl, clone_to_path)
        Migrate.removeLocalRepository(clone_to_path)
        repository_time_end = time.time()
        print("--- Repository Migration took %s seconds ---" % (repository_time_end - repository_time_start))
        print "########### Moving to next REPOSITORY! ###########\n\n"
    project_time_end = time.time()
    print("--- Project Migration took %s seconds ---" % (project_time_end - project_time_start))
    print "########### Completed Export of Project "+project['name']+" ###########"
