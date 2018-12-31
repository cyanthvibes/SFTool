"""
Author: Mariska Temming, S1106242
Summary: A class with the system specifications
"""


class System:
    def __init__(self, serial_number, disk_name, file_fomat):
        self.serial_number = serial_number
        self.disk_name = disk_name
        self.file_fomat = file_fomat

    def get_serial_number(self):
        return self.serial_number

    def get_disk_name(self):
        return self.disk_name

    def get_file_fomat(self):
        return self.file_fomat
