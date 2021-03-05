import re
import requests
import telegram
from umehinfo.Course import Course

class UmehBot:

    def __init__(self, token: str, message_id: int):
        self.bot = telegram.Bot(token=token)
        self.MESSAGE_ID = message_id
        self.messages = []

    def get_updates(self):
        '''
                MESSAGE :telegram.update

                {
                    'update_id': 414331608,
                    'message': {
                        'message_id': 566,
                        'date': 1614853183,
                        'chat': {
                            'id': 816329740,
                            'type': 'private',
                            'username': 'KuMeg',
                            'first_name': 'Kou',
                            'last_name': 'Mmi'
                            },
                        'text': 'ACCT1000',
                        'entities': [
                            {
                                'type': 'bot_command',
                                'offset': 0,
                                'length': 6
                                }
                            ],
                        'caption_entities': [],
                        'photo': [],
                        'new_chat_members': [],
                        'new_chat_photo': [],
                        'delete_chat_photo': False,
                        'group_chat_created': False,
                        'supergroup_chat_created': False,
                        'channel_chat_created': False,
                        'from': {
                            'id': 816329740,
                            'first_name': 'Ku',
                            'is_bot': False,
                            'last_name': 'Memi',
                            'username': 'Kg',
                            'language_code': 'zh-hans'
                        }
                    }
                }
                '''
        self.messages = self.bot.get_updates(offset=self.MESSAGE_ID)

    def update_message_id(self):
        self.set_message_id(self.messages[len(self.messages) - 1]['update_id'])

    def set_message_id(self, message_id):
        self.MESSAGE_ID = message_id

    def get_message_id(self) -> int:
        return self.MESSAGE_ID

    def send_message(self, chat_id: int, text: str, parse_mode: str, reply_markup: telegram.ReplyMarkup):
        return self.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)

    def is_message(self, message: telegram.Update) -> bool:
        # return (message.message is not None) or (message.edited_message is not None)
        return message.message is not None

    def is_text_message(self, message: telegram.Update) -> bool:
        return message.message.text is not None

    def is_command_message(self, message: telegram.Update) -> bool:
        for entity in message.message.entities:
            if entity.type == 'bot_command':
                return True
        return False

    def is_course_code(self, message: telegram.Update) -> bool:
        code=message.message.text.upper()
        return re.match(r'\w{4}\d{4}', code) or code == 'TEST'

    def if_course_exist(self, result: dict) -> bool:
        if result['course_info'] == 'Error Code':
            return False
        return True

    def get_course_info(self, code: str) -> dict:
        UMEH_SERVER = 'https://mpserver.umeh.top/'
        params = {
            'New_code': code,
        }
        path = UMEH_SERVER + 'course_info'
        r = requests.get(url=path, params=params)
        result = r.json()
        course=Course(self.if_course_exist(result),result)
        return course

    def send_course_info(self, chat_id: int, text: str, parse_mode: str, reply_markup: telegram.ReplyMarkup):
        return self.send_message(chat_id, text, parse_mode, reply_markup)
