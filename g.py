from github import Github
import os
g = Github(os.environ.get('GITHUB_TOKEN'))

def get_repos():
    response = []
    for repo in g.get_user().get_repos():
        response.append(repo.name)

    response ='\n'.join(response)
    return response