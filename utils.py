import re
from telegram import InlineKeyboardButton


def generate_course_keyboard(courses):
    keyboard = []
    num_in_row = 3
    row = []
    for i in range(len(courses)):
        if i % num_in_row == 0:
            keyboard.append(row)
            row = []
        row.append(courses[i]['New_code'])
    keyboard.append(row)
    return keyboard


def generate_prof_keyboard(profs):
    keyboard = []
    num_in_row = 3
    row = []
    for i in range(len(profs)):
        if i % num_in_row == 0:
            keyboard.append(row)
            row = []
        row.append(profs[i]['name'])
    keyboard.append(row)
    return keyboard


def generate_course_prof_keyboard(profs, code):
    keyboard = []
    num_in_row = 3
    row = []
    for i in range(len(profs)):
        if i % num_in_row == 0:
            keyboard.append(row)
            row = []
        row.append(InlineKeyboardButton(text=profs[i]['name'], callback_data='{}@{}'.format(code, profs[i]['name'])))
    keyboard.append(row)
    return keyboard


def generate_prof_markdown(prof):
    markdown = ''
    markdown += '*{}*\n'.format(prof['name'])
    markdown += '----------------------------\n'

    return markdown


def generate_course_keybord_of_prof_info(courses):
    keyboard = []
    num_in_row = 3
    row = []
    print(courses[0])
    for i in range(len(courses)):
        print(courses[i]['course_info']['New_code'])
        print(courses[i]['comment_info']['name'])
        if i % num_in_row == 0:
            keyboard.append(row)
            row = []
        row.append(InlineKeyboardButton(
            text=courses[i]['course_info']['New_code'],
            callback_data='{}@{}'.format(courses[i]['course_info']['New_code'], courses[i]['comment_info']['name'])))
    keyboard.append(row)
    return keyboard


def generate_course_info_markdown(course_info):
    markdown = ''
    markdown += '*{}*\n'.format(course_info['New_code'])
    markdown += '{}/{}\n'.format(course_info['Offering_Unit'], course_info['Offering_Department'])
    markdown += '*{}*\n'.format(course_info['courseTitleEng'])
    markdown += '{}\n'.format(course_info['courseTitleChi'])
    markdown += '{} Credits\n'.format(course_info['Credits'])
    markdown += '------------Description-----------\n'
    markdown += '{}\n'.format(course_info['courseDescription'])
    markdown += '------------Outcomes-----------\n'
    markdown += '{}\n'.format(course_info['Intended_Learning_Outcomes'])

    return markdown


def generate_prof_info_markdown(prof_info, code, comment_num):
    markdown = '*{}*\n'.format(code)
    markdown += '*{}*\n'.format(prof_info['name'])
    markdown += 'Overall: {:.2f}/5.9\n'.format(prof_info['result'])
    markdown += 'Grade: {:.2f}\n'.format(prof_info['grade'])
    markdown += 'Attendance: {:.2f}\n'.format(prof_info['attendance'])
    markdown += 'Hardness: {:.2f}\n'.format(prof_info['hard'])
    markdown += '----------------------------\n'
    markdown += '{} Comments'.format(comment_num)

    return markdown


def generate_comment_markdown(comment):
    markdown = ''
    markdown += '*{}*\n'.format(comment['content'])
    markdown += '----------------------------\n'

    return markdown


def check_code(code):
    """
    check the code is like 'ABCD1234' use regex
    """
    return re.match(r'[A-Z]{4}[0-9]{4}', code)
