import sys
from cli.core.CLI import Env


def echo(*text: str | int | bool | float, s: bool, silent: bool, repetitions: int) -> str:
    """
    Usage: echo <...text> [-s] [--repeat=<repetitions>]

    Prints the given text to the console.

    -s, --silent = Silent mode. Does not print the text to the console.
    --repetitions: int = The number of times to repeat the text.    
    """
    silent = silent or s

    result = " ".join(str(x) for x in text)

    if repetitions is not None:
        result = result * repetitions

    if not silent:
        print(result)

    return result


def exit(code: int = 0):
    """
    Usage: exit [code]

    Exits the CLI with the given exit code.
    """
    sys.exit(code)


def use(env: Env, lib: str):
    """
    Usage: use <library name>

    Imports the given library into the CLI.
    """
    env.include_library(lib)


def reload(env: Env):
    """
    Usage: reload

    Reloads all libraries that have been included into the evaluator.
    """
    print("Reloading...")
    env.reload_libraries()
    print("Reloaded.")
