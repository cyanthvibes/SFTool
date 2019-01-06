"""
Author: Mariska Temming, S1106242
Summary: Writes system/volume specifications (serial number, disk name and file format) to the database
"""

import wmi  # pip install wmi
from SFTool.database_helper import insert_data_system_specifications


# The class System contains system specifications: serial number, disk name and file fomat
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


# Writes system/volume specifications to the database
def register_system_specs_to_database():
    # Get the system specifications of every volume on the system
    for volume in wmi.WMI().Win32_LogicalDisk():
        disk_name = str(volume.Caption)
        serial_number = str(volume.VolumeSerialNumber)
        file_fomat = str(volume.FileSystem)

        system_specs = System(serial_number, disk_name, file_fomat)   # Creates a object system_specs
        # Print the system specifications on the console
        print("disk_name: " + system_specs.disk_name)
        print("file_fomat: " + system_specs.file_fomat)
        print("serial_number: " + system_specs.serial_number)
        insert_data_system_specifications(system_specs)   # Write the system specifications to the database
        print("\n")


def main():
    register_system_specs_to_database()


if __name__ == '__main__':
    main()

