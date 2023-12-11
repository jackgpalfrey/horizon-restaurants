from cli.core.CLI import Env
from src.utils.Database import Database


def init():
    """
    Usage: init
    """
    Database.connect()
    return True


def prompt(env: Env):
    prompt = ""

    if Database.connection.info.dbname is not None:
        prompt += f"{Database.connection.info.dbname}"

    if env.get_ctx("username") is not None:
        prompt += f" @ {env.get_ctx('username')}"

    prompt += " > "

    return prompt
