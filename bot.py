import telegram


class UmehBot:

    def __init__(self, token, message_id):
        self.bot = telegram.Bot(token=token)
        self.MESSAGE_ID = message_id
        self.message = []

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
        self.message = self.bot.get_updates(offset=self.MESSAGE_ID)

    def update_message_id(self):
        self.MESSAGE_ID = self.message[len(self.message) - 1]['update_id']

    def get_message_id(self):
        return self.MESSAGE_ID

    def send_message(self, chat_id: int = 0, text: str = ''):
        pass
