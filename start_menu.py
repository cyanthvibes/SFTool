"""
Author: Mariska Temming, S1106242
Summary: - The startmenu is the main of the SFTool
         - It shows the GUI of the SFTool
         - The user could choose three options in the GUI: "Quit", "Create memory dump" and "Start malware scan"
         - When the user clicks on "Start malware scan", SFTool is scanning the system of availability of malware
         - When the user clicks on "Create memory dump", SFTool runs MagnetRAMCapture
         - When the user clicks on "Quit", the GUI closes

Update: Daan Schellingerhoudt, s1108356
    -added creating_memory_dump
    -added file and folder scan to the start_menu
"""


import PySimpleGUI as sg  # pip install PySimpleGUI
import datetime
from time import sleep
import subprocess
import sys

from case import Case
from database_helper import insert_data_case_information
from sys_specs import register_system_specs_to_database
from hashing import get_pathname_and_hashes, hashing_without_limitations, convert_md5_to_sha1, hash_single_file
from hashing import hash_single_folder, hash_folder_limited_size
from compare_hashes import compare_hashes
from network_checker import internet_on
from virustotal import register_malware_to_database
from malware_copy import malware_copy

# Logs everything from the console to a text file
sys.stdout = open('console_log.txt', 'w')


# Update the status mode in the GUI
def update_status_mode(window, status_mode):
    window.FindElement('_STATUS_').Update(status_mode)
    window.Refresh()
    sleep(1)


# Starts the program MagnetRAMCapture.exe and hides the GUI while it runs
def creating_memory_dump(window):
    window.Hide()
    subprocess.call(['MagnetRAMCapture.exe'], shell=True)
    window.UnHide()


# The function scan malware is the main program of the SFTool: SFTool is scanning the system of availability of malware
def scan_malware(window, file_size, single_file, single_folder):
    try:
        print("The malware scan has been started" + "\n")
        update_status_mode(window, "The malware scan has been started")

        print('Registrating the system specifications... ' + "\n")
        update_status_mode(window, "Registrating the system specifications... ")
        register_system_specs_to_database()  # Write system specifications to database

        if file_size == 0 and single_file == '' and single_folder == '':
            print('Calculating hashes... ' + "\n")
            update_status_mode(window, "Calculating hashes...")
            hashing_without_limitations()  # Calculate the md5 hashes of the files on the system

        elif file_size != 0 and single_folder != '':
            print('Calculating hashes... ' + "\n")
            update_status_mode(window, "Calculating hashes...")
            hash_folder_limited_size(file_size, single_folder)  # Calculate the md5 hashes of the files on the of the selected folder

        elif file_size != 0:
            print('Calculating hashes... ' + "\n")
            update_status_mode(window, "Calculating hashes...")
            get_pathname_and_hashes(file_size)  # Calculate the md5 hashes of the files on the system

        elif single_folder != '':
            print('Calculating hashes... ' + "\n")
            update_status_mode(window, "Calculating hashes...")
            hash_single_folder(single_folder)  # Calculate the md5 hashes of the selected folder

        elif single_file != '':
            print('Calculating hashes... ' + "\n")
            update_status_mode(window, "Calculating hashes...")
            hash_single_file(single_file)  # Calculate the md5 hash of the selected file

        print('Comparing system hashes with VirusShare... ' + "\n")
        update_status_mode(window, "Comparing system hashes with VirusShare... ")
        malware_found = compare_hashes()  # Offline database: virusshare (compare system hashes with the hahses of
        # VirusShare)

        if malware_found:
            print('Converting MD5 to SHA1...' + "\n")
            update_status_mode(window, "Converting MD5 to SHA1...")
            convert_md5_to_sha1()  # Converts the malware md5 hashes to sha1

            # Check if the system has an connection to the internet
            if internet_on():
                print('The system is connected to the internet!' + "\n")
                update_status_mode(window, "The system is connected to the internet!")

                print("\n" + 'Checking malware name in VirusTotal... ' + "\n")
                update_status_mode(window, "Checking malware name in VirusTotal...  ")
                register_malware_to_database()  # Online database: VirusTotal (writes the malware information to the
                # database)

            print('Copying malware to USB drive...')
            update_status_mode(window, "Copying malware to USB drive...")
            malware_copy()  # Copies the malware to dictionary "malware_copies" on the USB-drive

            print('The malware scan has finished: malware found!')
            update_status_mode(window, "The malware scan has finished: malware found!")

        else:
            print('The malware scan has finished: no malware found!' + "\n")
            update_status_mode(window, "The malware scan has finished: no malware found!")

    except Exception as e:
        print(e)
        update_status_mode(window, e)


# Shows the GUI of the SFTool
def show_window():
    status_mode = sg.Text('Welcome!', size=(45, 1), font=('Arial', 14), text_color='red', key='_STATUS_')
    empty_row = sg.Text('', size=(1, 1))  # creates a empy row for the format of the GUI
    # create buttons
    start_malware = sg.Button('Start malware scan', size=(17, 1), font=('Arial', 18), button_color=('black', 'white'),
                              enable_events=True, )
    create_memory_dump = sg.Button('Create memory dump', size=(17, 1), font=('Arial', 18), button_color=('black', 'white'),
                              enable_events=True, )
    quit_startmenu = sg.Button('Quit', size=(5, 1), font=('Arial', 18), button_color=('black', 'white'))

    # Layout the design of the GUI
    layout = [
        [sg.Text('SFTool - Synergy Forensics Triage Tool', size=(31, 2), text_color='blue', font=('Arial', 30))],
        [sg.Text('Case information', size=(15, 1), font=('Arial', 16, 'bold'))],
        [sg.Text('Case Name:', size=(15, 1), font=('Arial', 14)), sg.InputText(key='_CASE_NAME_', font=('Arial', 14))],
        [sg.Text('Start Number:', size=(15, 1), font=('Arial', 14)), sg.InputText(key='_START_NUMBER', font=('Arial', 14))],
        [sg.Text('Investigator:', size=(15, 1), font=('Arial', 14)), sg.InputText(key='_INVESTIGATOR_', font=('Arial', 14))],
        [sg.Text('Comment:', size=(15, 1), font=('Arial', 14)), sg.InputText(key='_COMMENT_', font=('Arial', 14))],
        [empty_row],
        [sg.Text('Filters', size=(15, 1), font=('Arial', 16, 'bold'))],
        [sg.Text('File Size Limit (MB):', size=(15,1), font=('Arial', 14)), sg.InputText(key='_FILE_SIZE_', font=('Arial', 14))],
        [sg.FileBrowse(key='_FILE_NAME_', font=('Arial', 14), size=(15, 1)), sg.InputText('Select single file to scan', font=('Arial', 14))],
        [sg.FolderBrowse(key='_FILE_FOLDER_', font=('Arial', 14), size=(15, 1)), sg.InputText('Select single folder to scan', font=('Arial', 14))],
        [empty_row],
        [sg.Text('Status: ', size=(15, 1), font=('Arial', 14)), status_mode],
        [empty_row],
        [empty_row],
        [quit_startmenu, empty_row, create_memory_dump, empty_row, start_malware],
        [empty_row]
    ]

    window = sg.Window('SFT - Start menu').Layout(layout)  # Shows the window to the user

    while True:
        event, value = window.Read() # Read the Window
        # Take appropriate action based on button
        if event == 'Create memory dump':
            creating_memory_dump(window)

        elif event == 'Start malware scan':
            case_name = value['_CASE_NAME_']
            start_number = value['_START_NUMBER']
            investigator_name = value['_INVESTIGATOR_']
            comment = value['_COMMENT_']
            file_size = value['_FILE_SIZE_']
            time = datetime.datetime.now()
            single_file = value['_FILE_NAME_']
            single_folder = value['_FILE_FOLDER_']

            # If case information is not filled then show a pop up
            if case_name == '' or start_number == '' or investigator_name == '':
                sg.Popup("Fill in the case data on the start menu. " + "\n" +
                         "Required: case name, start number and investigator's name" + "\n")
                print("Fill in the case data on the start menu. " + "\n" +
                      "Required: case name, start number and investigator's name" + "\n")

            # Else if file size is not a number and not empty, then show a pop up
            elif not file_size.isdigit() and file_size != "":
                sg.Popup("Please fill in a number for the file size(MB)")
                print("Please fill in a number for the file size(MB)")

            elif single_file != '' and single_folder != '':
                sg.Popup("Please select only one of the following options: 'Select single file "
                         "to scan' or ' Select single folder to scan'")
                print("Please select only one of the following options: 'Select single file "
                      "to scan' or ' Select single folder to scan'")

            elif file_size != '' and single_file != '':
                sg.Popup("It is not possible to select a file size while scanning a single file")
                print("It is not possible to select a file size while scanning a single file")

            # Else start the malware scan
            else:
                if file_size == '':     # If file size is not filled by the user then file size = 0 (scan whole system)
                    file_size = 0

                file_size = int(file_size)
                single_file = str(single_file)
                single_folder = str(single_folder)
                print("Time: " + str(time))
                print("Event: " + event + "\n" + "\n", "Case Name: " + "\t" + case_name + "\n",
                      "Start Number: " + "\t" +
                      start_number + "\n", "Investigator: " + "\t" + investigator_name + "\n", "Comment: " +
                      "\t" + "\t" + comment + "\n")

                case_data = Case(case_name, start_number, investigator_name, comment, time)
                insert_data_case_information(case_data)  # Write case information to database

                scan_malware(window, file_size, single_file, single_folder)

        elif event == 'Quit' or event is None:
            window.Close()
            break

    return window


def sftool():
    try:
        show_window()
    except Exception as e:
        print(e)


def main():
    sftool()


if __name__ == '__main__':
    main()
