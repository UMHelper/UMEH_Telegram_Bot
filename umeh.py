import requests

UMEH_SERVER = 'https://mpserver.umeh.top'

def get_course_info(code):
    params = {
        'New_code': code
    }
    req = requests.get("{}/course_info".format(UMEH_SERVER), params=params)
    return req.json()

def fuzzy_search(text, type):
    params = {
        'text': text,
        'type': type
    }
    req = requests.get("{}/fuzzy_search".format(UMEH_SERVER), params=params)
    return req.json()

def get_comment_info(prof,code):
    params = {
        'prof_name': prof,
        'New_code': code
    }
    req = requests.get("{}/all_comment_info".format(UMEH_SERVER), params=params)
    return req.json()

if __name__ == '__main__':
    res=fuzzy_search('acc', 'course')
    for i in res['course_info']:
        print(i['New_code'])
