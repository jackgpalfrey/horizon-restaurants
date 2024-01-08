# Author: Dina Hassanein (22066792)
import requests

URL = "http://localhost:5000"
API = requests.Session()


class State:
    branch_id = None
    username = None
    is_ui_rendered = False
