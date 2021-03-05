import telegram


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
                        'entities': [],
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
        self.MESSAGE_ID = self.messages[len(self.messages) - 1]['update_id']

    def get_message_id(self) -> int:
        return self.MESSAGE_ID

    def send_message(self, chat_id: int, text: str, parse_mode: str, reply_markup: telegram.ReplyMarkup):
        return self.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)

    def is_text_message(self, message: telegram.Update) -> bool:
        pass

    def is_command_message(self, message: telegram.Update) -> bool:
        pass

    def is_course_code(self, message: telegram.Update) -> bool:
        pass

    def if_course_exist(self, result: dict) -> bool:
        pass

    def get_course_info(self, code: str) -> dict:
        pass

    def send_course_info(self, chat_id: int, text: str, parse_mode: str, reply_markup: telegram.ReplyMarkup):
        return self.send_message(chat_id, text, parse_mode, reply_markup)
