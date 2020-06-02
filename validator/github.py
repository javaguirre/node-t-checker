import json

from github import Github

from .types import PublishableOutput


class GithubEvent:
    @staticmethod
    def get_pull_request_id(event_path: str) -> int:
        pull_request_id = None

        with open(event_path, 'r') as file:
            event = json.loads(file.readlines())
            pull_request_id = event['number']
        return pull_request_id


class GithubService(PublishableOutput):
    REPOSITORY = 'alastria/alastria-node'

    def __init__(self, token: str):
        self.client = Github(token)
        self.repo = self.client.get_repo(self.REPOSITORY)
        self.pull_request_id = None

    def use_pull_request_id(self, pull_request_id: int) -> None:
        self.pull_request_id = pull_request_id

    def get_pr_description(self, pull_request_id: int) -> str:
        data = self.repo.get_pull(self.pull_request_id)
        return data.body

    def publish(self, body: str) -> None:
        data = self.repo.get_pull(self.pull_request_id)
        data.create_comment(body)
