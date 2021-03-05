import logging

import requests
from .Instructor import Instructor

class Course:

    def __init__(self, result):
        course_info=result['course_info']
        prof_info=result['prof_info']
        self.new_code = course_info['New_code']
        self.offering_unit = course_info['Offering_Unit']
        self.old_code = course_info['Old_code']
        self.course_title_eng = course_info['courseTitleEng']
        self.course_title_chi = course_info['courseTitleChi']
        self.credits = course_info['Credits']
        self.medium_of_instruction = course_info['Medium_of_Instruction']
        self.offering_department =course_info['Offering_Department']
        self.instructors = []
        for prof in prof_info:
            self.instructors.append(Instructor(prof))
