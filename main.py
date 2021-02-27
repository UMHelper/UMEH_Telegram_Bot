import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))

API_TOKEN = ''
API_SERVER = ''
PORT = 0


def load_setting():
    try:
        with open(os.path.join(DIR, "config.json")) as config_json:
            config = json.load(config_json)
    except FileNotFoundError:
        print("No Config")
    return config["API_TOKEN"], config["API_SERVER"], config["PORT"]
