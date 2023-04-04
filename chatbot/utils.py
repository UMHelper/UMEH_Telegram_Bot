import os

import requests


def get_comment_path(course_code, prof_name):
    path=os.path.join(os.getcwd(), 'comment', course_code, prof_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_index_path(course_code, prof_name):
    path=os.path.join(os.getcwd(), 'index', course_code)
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(os.getcwd(), 'index', course_code, prof_name)
    return path

def get_course_info(code):
    params = {
        'New_code': code
    }
    req = requests.get("{}/course_info".format('https://mpserver.umeh.top'), params=params)
    return req.json()['course_info']