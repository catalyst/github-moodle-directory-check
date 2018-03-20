import requests
from github import Github

from app.repository import Repository


class GithubConnector:
    def __init__(self, token, repository_owner):
        self.github = Github(token)
        self.owner = repository_owner

    def fetch_repositories(self):
        for repository in self.github.get_user(self.owner).get_repos():
            yield Repository(repository.name)

    def get_file(self, repository, file):
        link = "https://github.com/" + self.owner + "/" + repository + "/raw/HEAD/" + file
        data = requests.get(link)
        if data.status_code != 200:
            return None
        return data.text
