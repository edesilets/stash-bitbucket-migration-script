import stashy

class Stash():
    def __init__(self, host, username, password):
        # To stop ssl check use verify=False as the last parameter 
        self.stash = stashy.connect(host, username, password)

    def getProjects(self):
        return self.stash.projects.list()

    def getProjectRepositories(self, project_key):
        return self.stash.projects[project_key].repos