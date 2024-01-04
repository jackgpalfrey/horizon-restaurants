"""Production initialisation module."""
from .utils.Database import Database
from .user.UserService import UserService
from .api.main import main as api_main


def main():
    Database.connect()
    Database.init()

    UserService.init()

    api_main()
