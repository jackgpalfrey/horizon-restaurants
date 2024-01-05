import requests

URL = "http://localhost:5000"
API = requests.Session()


class State:
    branch = None
    username = None
