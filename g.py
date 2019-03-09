from github import Github
g = Github("864faa783c3943a73ab37f17547a6d70329130f9")

def get_repos():
    response = []
    for repo in g.get_user().get_repos():
        response.append(repo.name)

    response ='\n'.join(response)
    return response