from dataclasses import dataclass


@dataclass()
class CLIError(Exception):
    message: str


class ParseError(CLIError):
    pass


class ArgError(CLIError):
    pass


class CommandError(CLIError):
    pass
