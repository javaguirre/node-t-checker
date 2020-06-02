#!/usr/bin/env python
import os

import click

from .validator import NodeValidator
from .formatter import ValidatorOutputFormatter
from .types import ValidatorOutput
from .github import GithubService


@click.command()
def validate():
    pull_request_id: int = os.environ.get('TRAVIS_PULL_REQUEST')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

    if not pull_request_id:
        return

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
