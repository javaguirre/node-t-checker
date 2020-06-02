from dataclasses import dataclass


@dataclass
class SubprocessOutputMock:
    returncode: int
    stdout: str
