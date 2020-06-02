#!/usr/bin/env python
import os

import click

from .validator import NodeValidator
from .formatter import ValidatorOutputFormatter
from .types import ValidatorOutput
from .github import GithubService, GithubEvent


@click.command()
def validate():
    GITHUB_EVENT_NAME = os.environ.get('GITHUB_EVENT_NAME')

    if GITHUB_EVENT_NAME != 'pull_request':
        return

    GITHUB_EVENT_PATH = os.environ.get('GITHUB_EVENT_PATH')
    pull_request_id: int = GithubEvent.get_pull_request_id(GITHUB_EVENT_PATH)
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

    github_service = GithubService(GITHUB_TOKEN)
    github_service.use_pull_request_id(pull_request_id)
    node_info = github_service.get_node_info()
    output: ValidatorOutput = NodeValidator(node_info).get_validation()
    output_formatter = ValidatorOutputFormatter(github_service, output)
    message = output_formatter.get_message()

    if output.has_errors():
        output_formatter.publish_errors(message)
        return

    output_formatter.publish_success_message(message)


if __name__ == '__main__':
    validate()
