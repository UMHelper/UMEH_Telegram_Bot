import json
import os
import requests

DIR = os.path.dirname(os.path.abspath(__file__))
API_SERVER = "https://api.telegram.org/bot"


def load_setting():
    try:
        with open(os.path.join(DIR, "config.json")) as config_json:
            config = json.load(config_json)
    except FileNotFoundError:
        print("No Config")
    return config["API_TOKEN"], config["UMEH_SERVER"], config["PORT"]


API_TOKEN, UMEH_SERVER, PORT = load_setting()


def get_update(offset=0):
    r=requests.get(API_SERVER+API_TOKEN+"/getUpdates?offset="+str(offset))
    r.json()


def main():
    get_update()


if __name__ == '__main__':
    main()
