import json
import os

import requests

DIR = os.path.dirname(os.path.abspath(__file__))
API_SERVER = "https://api.telegram.org/bot"


def load_config():
    try:
        with open(os.path.join(DIR, "config.json")) as config_json:
            config = json.load(config_json)
    except FileNotFoundError:
        print("No Config")
    return config["API_TOKEN"], config["UMEH_SERVER"], config["PORT"], config["MESSAGE_ID"], config


API_TOKEN, UMEH_SERVER, PORT, MESSAGE_ID, CONFIG_DIC = load_config()


def config_update( message_id):
    try:
        with open(os.path.join(DIR, "config.json"), 'w+') as config_json:
            CONFIG_DIC["MESSAGE_ID"] = message_id
            json.dump(CONFIG_DIC, config_json)
            config_json.close()
    except FileNotFoundError:
        print("No Config")


'''
    :param offset Integer
        the newest message id in last update
'''


def get_updates(offset=0):
    r = requests.get(API_SERVER + API_TOKEN + "/getUpdates?offset=" + str(offset))
    '''
        :var messages List
            Message list beginning with the latest message of last update
    '''

    '''
            Example:
            [
                {
                    'update_id' : 414331188,
                    'message' : {
                        'message_id'  4，
                        ‘from’ : {
                            'id' : 81632974,
                            'is_bot' : false
                            'first_name' : 'Kou',
                            'last_name' : 'Mei',
                            'username': 'KouMei',
                            'language_code' : 'zh-hans
                        },
                        'chat' : {
                            'id' : 81632974,
                            'is_bot' : false
                            'first_name' : 'Kou',
                            'last_name' : 'Mei',
                            'username': 'KouMei',
                            'type' : 'private'
                        },
                        date : 1614458067,
                        text : 'text'
                    }
                },
                {},{},{}...
            ]
    '''
    messages = r.json()["result"]
    latest_message_id = messages[len(messages) - 1]['update_id']

# def main():
#     get_update()
#
#
# if __name__ == '__main__':
#     main()
