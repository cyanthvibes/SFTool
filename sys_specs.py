"""
Author: Mariska Temming, S1106242
Summary: Write system/volume specifications (serial number, disk name and file format) to the database
"""

import wmi  # pip install wmi
from SFTool.system import System
from SFTool.database_helper import insert_data_system_specifications


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
