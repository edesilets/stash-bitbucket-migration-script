#!/usr/bin/python
import stashy
import migrate
import tools

class Stash():
    def __init__(self, host, username, password):
        self.stash = stashy.connect(host, username, password)
        self.tools = tools.Tools()

    def getProjects(self):
        return self.stash.projects.list()

    def getProjectRepositories(self, project_key):
        return self.stash.projects[project_key].repos

    def gatherInformation(self):
        self.repository_information = {}
        for project in self.getProjects():
            projectsRepos = self.getProjectRepositories(project['key'])
            project_repositories = projectsRepos.list()

            self.repository_information[project['key']] = {
                "name": project["name"],
                "repositories": []
            }

            for repository in project_repositories:
                # TODO: move find git ssh url to tools service.... or something.
                stash_git_url = self.tools.findGitSSHURL(repository['links']['clone'])
                self.repository_information[project['key']]["repositories"].append({
                    repository['name']: stash_git_url
                })
        return self.repository_information