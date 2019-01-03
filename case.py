"""
Author: Mariska Temming, S1106242
Summary: A class with the case information
"""


class Case:
    def __init__(self, case_name, start_number, investigator_name, comment, time):
        self.case_name = case_name
        self.start_number = start_number
        self.investigator_name = investigator_name
        self.comment = comment
        self.time = time

    def get_case_name(self):
        return self.case_name

    def get_start_number(self):
        return self.start_number

    def get_investigator_name(self):
        return self.investigator_name

    def get_comment(self):
        return self.comment

    def get_time(self):
        return self.time
