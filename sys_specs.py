"""
Author: Mariska Temming, S1106242
Summary: Write system specifications (serial number, disk name and file format) to the database
"""

import wmi  # pip install wmi
from SFTool.system import System
from SFTool.database_helper import insert_data_system_specifications


def register_system_specs_to_database():

    c = wmi.WMI()
    for pm in c.Win32_Volume():
        disk_name = str(pm.wmi_property('DriveLetter').value)
        serial_number = str(pm.wmi_property('SerialNumber').value)
        file_fomat = str(pm.wmi_property('FileSystem').value)

        system_specs = System(serial_number, disk_name, file_fomat)
        print("disk_name: " + system_specs.disk_name)
        print("file_fomat: " + system_specs.file_fomat)
        print("serial_number: " + system_specs.serial_number)

        insert_data_system_specifications(system_specs)


def main():
    register_system_specs_to_database()


if __name__ == '__main__':
    main()
