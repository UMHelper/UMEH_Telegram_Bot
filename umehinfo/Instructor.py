import requests
from .Review import Review


class Instructor:
    def __init__(self, prof_info: dict, code: str):
        self.code = code
        self.name = prof_info['name']
        self.result = prof_info['result']
        self.grade = prof_info['grade']
        self.attendance = prof_info['attendance']
        self.hard = prof_info['hard']
        self.reward = prof_info['reward']
        self.num = prof_info['num']
        self.review = []

    def get_review(self):
        UMEH_SERVER = 'https：//mpserver.umeh.top/'
        params = {
            'New_code': self.code

        }
        path = UMEH_SERVER + 'course_info'
        r = requests.get(url=path, params=params)
        result = r.json()
        comments = result['comments']
        for comment in comments:
            self.review.append(Review(comment))
