from src.utils.Database import Database


def init():
    """
    Usage: init
    """
    Database.connect()
    return True


def prompt():
    return "horizon > "
