# Author: Jack Palfrey (22032928)
"""Module for managing enviroment variables."""
import os


def get_env(key: str):
    """Get given enviroment variable."""
    return os.environ[key]
