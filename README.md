# Stash Export tool

## Configuration
Copy and rename `.env.example` to  `.env`. Inside of this `.env` populate the environment variables.

### Description of Environment Variables that Could be Confusing
- STASH_SSH_KEY_PATH="~/.ssh/"

Any env var that has `*_SSH_KEY_PATH` should be set to the path of the ssh key form the users home directory. Your key path for Stash and BitBucket might be the same and that's just fine.


- BITBUCKET_SSH_CONFIG_HOSTNAME="puppies"

Any env var that has `*_SSH_CONFIG_HOSTNAME` should be set to the host name from your `~/.ssh/config`

Example of inside of `~/.ssh/config`
```
Host puppies
    User git
    Port 9091
    HostName bitbucket.server.hello.com
    IdentityFile ~/.ssh/puppiesGit
```

- BITBUCKET_DEFAULT_GROUP=""

Check your bitbucket server for a group that you would like to set as the project and repository default group.

- BITBUCKET_DEFAULT_USER=""

This user should be in the users list in setting in your bitBucket server.

- BITBUCKET_DEFAULT_PERMISSION="admin"

Three permissions levels available are `read`, `write`, and `admin`. This will set the permission on project level and repository level.

## Versions
- Python 2.7.13

### PIP Packages
Developed with the following packages

- stashy==0.3
- urllib3==1.22
- requests==2.18.4
- GitPython==2.1.8
- python-dotenv==0.7.1


https://github.com/cosmin/stashy
