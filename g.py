from github import Github
import os
g = Github(os.environ.get('GITHUB_TOKEN'))

def get_repos(user):
    repos = g.get_user(user).get_repos()
    return responsify(repos)

def get_repo(user, repoName):
    return g.get_user(user).get_repo(repoName)

def get_branches(user, repoName):
    repo = g.get_user(user).get_repo(repoName)
    branches = repo.get_branches()

    return responsify(branches)

def responsify(items):
    response = []
    for item in items:
        response.append(item.name)

    response ='\n'.join(response)
    return '```' + response + '```'