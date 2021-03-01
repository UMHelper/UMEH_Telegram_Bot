import json
import os
import re
import requests
import time
import logging

logging.basicConfig(filename='log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DIR = os.path.dirname(os.path.abspath(__file__))
API_SERVER = "https://api.telegram.org/bot"


def load_config():
    try:
        with open(os.path.join(DIR, "config.json")) as config_json:
            config = json.load(config_json)
            logging.info("Config load successfully, bot start")
            logging.info('------------------------------------------')
    except FileNotFoundError:
        logging.error('Config file Error')
        logging.info('------------------------------------------')
    return config["API_TOKEN"], config["UMEH_SERVER"], config["PORT"], config


API_TOKEN, UMEH_SERVER, PORT, CONFIG_DIC = load_config()


def config_update():
    try:
        with open(os.path.join(DIR, "config.json"), 'w+') as config_json:
            json.dump(CONFIG_DIC, config_json)
            config_json.close()
    except FileNotFoundError:
        logging.error('Config file Error')
        logging.info('------------------------------------------')


messages = []


def send_message(text, chat_id):
    path = API_SERVER + API_TOKEN + '/sendmessage'
    message = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown',
    }
    r = requests.get(url=path, params=message)
    logging.info('Send Message to ' + str(chat_id) + ' successfully')


def get_course_info(code):
    params = {
        'New_code': code
    }
    path = UMEH_SERVER + 'course_info'
    r = requests.get(url=path, params=params)
    result = r.json()
    logging.info('Get ' + code + ' info successfully')
    return result


def is_key_in_dic(dic, key):
    return key in dic


def is_course_code(code):
    return re.match(r'\w{4}\d{4}', code)


def is_text_message(message):
    return is_key_in_dic(message, 'message') and is_key_in_dic(message['message'], 'text') and (len(message['message']['text']) < 20)


def course_exist(result):
    return result['course_info'] != 'Error Code'


def process_message(message):
    text = ''
    if is_text_message(message):
        chat_id = message['message']['chat']['id']
        logging.info('Process request from ' + message['message']['from']['username'] + ', chat id is ' + str(chat_id))
        code = message['message']['text'].upper()
        if is_course_code(code):
            result = get_course_info(code)
            if course_exist(result):
                text = "Click here to visit our website👉[" + code + "](https://umeh.top/course/" + code + ")"
            else:
                text = "Search Code: " + code + "\nResult : Code doesn't exist"
            send_message(text, chat_id)
        logging.info('------------------------------------------')


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
    while True:
        get_updates()
        process_all_messages()
        time.sleep(1)


if __name__ == '__main__':
    main()
