import os
import re
import logging
import json
import subprocess

from .types import NodeInformation, ValidatorOutput


class NodeValidator():
    REGULAR_DIRECTORY_PATH = 'DIRECTORY_REGULAR.md'

    PUBLIC_IP_REGEX = r'21000/tcp\s+(open|filtered)'
    NODE_EUROPE_REGEX = r'country:\s+EU'

    def __init__(self, node_info: NodeInformation):
        self.node_info = node_info

    def get_validation(self) -> ValidatorOutput:
        # TODO How to check if the new is in netstats in red?
        with open('data/validator-nodes', 'r') as file:
            is_validator_valid=self.is_valid_json_file(file.readlines())
        with open('data/constellation-nodes.json', 'r') as file:
            is_constellation_valid=self.is_valid_json_file(file.readlines())
        with open('data/regular-nodes.json', 'r') as file:
            is_regular_valid=self.is_valid_json_file(file.readlines())

        return ValidatorOutput(
            is_ip_public=self.is_ip_public(),
            is_node_in_europe=self.is_node_in_europe(),
            is_geth_version_valid=self.is_geth_version_valid(),
            is_validator_valid=is_validator_valid,
            is_constellation_valid=is_constellation_valid,
            is_regular_valid=is_regular_valid,
            is_enode_in_directory_valid=self.has_valid_enode_and_ip_in_regular_directory()
        )

    def is_ip_public(self) -> bool:
        output = subprocess.run(
            f'nmap {self.node_info.ip} -p 21000',
            shell=True,
            capture_output=True
        )

        if output.returncode != 0:
            return False

        return bool(
            re.search(
                self.PUBLIC_IP_REGEX,
                output.stdout.decode('utf-8')
            )
        )

    def is_node_in_europe(self) -> bool:
        output = subprocess.run(
            f'whois -h whois.ripe.net {self.node_info.ip}',
            shell=True,
            capture_output=True
        )

        if output.returncode != 0:
            return False

        return bool(
            re.search(
                self.NODE_EUROPE_REGEX,
                output.stdout.decode('utf-8')
            )
        )

    def is_valid_json_file(self, file_output: str, fake_json: bool = False) -> bool:
        '''
            fake_json: It seems there are some files with a json extension
            and aren\'t JSON :scream:
        '''

        if fake_json:
            file_output = f'[ {file_output} ]'

        try:
            json.loads(file_output)
        except ValueError:
            return False
        return True

    def check_valid_node_in_regular_directory(self):
        with os.open(self.REGULAR_DIRECTORY_PATH, 'r') as file:
            file_output = file.readlines()
            # TODO
