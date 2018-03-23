import sys

class Tools():
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
