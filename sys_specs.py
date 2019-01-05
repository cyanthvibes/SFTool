"""
Author: Mariska Temming, S1106242
Summary: Write system/volume specifications (serial number, disk name and file format) to the database
"""

import wmi  # pip install wmi
from SFTool.database_helper import insert_data_system_specifications


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


def register_system_specs_to_database():
    for volume in wmi.WMI().Win32_LogicalDisk():
        disk_name = str(volume.Caption)
        serial_number = str(volume.VolumeSerialNumber)
        file_fomat = str(volume.FileSystem)

        system_specs = System(serial_number, disk_name, file_fomat)     # creates a object system_specs
        print("disk_name: " + system_specs.disk_name)
        print("file_fomat: " + system_specs.file_fomat)
        print("serial_number: " + system_specs.serial_number)
        insert_data_system_specifications(system_specs)     # write the system specifications to the database
        print("\n")


def main():
    register_system_specs_to_database()


if __name__ == '__main__':
    main()
