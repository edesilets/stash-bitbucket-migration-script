#!/usr/bin/python
import stashy
import migrate

class Stash():
    def __init__(self, host, username, password):
        self.stash = stashy.connect(host, username, password)

    def getProjects(self):
        return self.stash.projects.list()

    def getProjectRepositories(self, project_key):
        return self.stash.projects[project_key].repos

    def gatherStashInformation(self):
        self.repository_information = {}
        for project in self.getProjects():
            projectsRepos = self.getProjectRepositories(project['key'])
            project_repositories = projectsRepos.list()

            self.repository_information[project['key']] = {
                "project": project["name"],
                "repositories": []
            }

            for repository in project_repositories:
                # TODO: move find git ssh url to tools service.... or something.
                stash_git_url = migrate.Migrate.findGitSSHURL(repository['links']['clone'])
                self.repository_information[project['key']]["repositories"].append({
                    repository['name']: stash_git_url
                })
        return self.repository_information