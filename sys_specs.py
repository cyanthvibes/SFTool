"""
Author: Mariska Temming, S1106242
Summary: Write system specifications (serial number, disk name and file format) to the database
"""

import wmi  # pip install wmi
import psutil   # pip install psutil
from SFT.system import System
from SFT.database_helper import insert_data_system_specifications


def register_system_specs_to_database():
    for part in psutil.disk_partitions():
        disk_name = part.device
        file_fomat = part.fstype

        c = wmi.WMI()
        for pm in c.Win32_PhysicalMedia():
            serial_number = pm.SerialNumber

            system_specs = System(serial_number, disk_name, file_fomat)
            print("System specifications: ")
            print("serial_number: " + pm.SerialNumber)
            print("disk_name: " + system_specs.disk_name)
            print("file_fomat: " + system_specs.file_fomat)
            insert_data_system_specifications(system_specs)


def main():
    register_system_specs_to_database()


if __name__ == '__main__':
    main()
