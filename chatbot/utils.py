import os


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