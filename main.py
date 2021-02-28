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
    return config["API_TOKEN"], config["UMEH_SERVER"], config["PORT"], config


API_TOKEN, UMEH_SERVER, PORT, CONFIG_DIC = load_config()


def config_update():
    try:
        with open(os.path.join(DIR, "config.json"), 'w+') as config_json:
            json.dump(CONFIG_DIC, config_json)
            config_json.close()
    except FileNotFoundError:
        print("No Config")


messages = []

def convert_list_to_string(l):
    return ','.join(l)
def send_message(text, chat_id):
    path = API_SERVER + API_TOKEN + '/sendmessage'
    message = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown',
    }
    print(message)
    r= requests.get(url=path, params=message)
    print(r.url)


def get_course_info(code):
    params = {
        'New_code': code
    }
    path = UMEH_SERVER + 'course_info'
    r = requests.get(url=path, params=params)
    result = r.json()
    print(result)
    return result


def is_text_message(message):
    if 'text' in message['message']:
        return True
    return False


def is_code(result):
    if result['course_info'] == 'Error Code':
        return False
    return True


def process_message(message):
    text = ''
    chat_id = message['message']['chat']['id']
    if is_text_message(message):
        code = message['message']['text'].upper()
        result = get_course_info(code)
        if is_code(result):
            text = "Click here to visit our website👉[" + code + "](https://umeh.top/course/" + code + ")"
        else:
            text = "Search Code: " + code + "\nResult : Code doesn't exist"
        send_message(text, chat_id)


def process_all_messages():
    if len(messages) > 1:
        for i in range(1, len(messages)):
            process_message(messages[i])


def get_updates():
    '''
        :param offset Integer
            the newest message id in last update
    '''
    path = API_SERVER + API_TOKEN + "/getUpdates?offset=" + str(CONFIG_DIC["MESSAGE_ID"])
    r = requests.get(path)
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
    global messages
    messages = r.json()["result"]
    CONFIG_DIC["MESSAGE_ID"] = messages[len(messages) - 1]['update_id']
    config_update()


def main():
    pass


if __name__ == '__main__':
    main()
