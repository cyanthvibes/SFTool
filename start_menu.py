"""
Author: Mariska Temming, S1106242
Summary: - The startmenu is the main of the SFTool.
         - First it makes a memory dump of the system.
         - Then it shows the GUI of the SFTool.
         - The user could choose three options in the GUI: "View database", "Quit" and "Start malware scan".
         - When the user clicks on "Start malware scan", SFTool is scanning the system of availability of malware.
         - When the user clicks on "View database", the database (SFT.db) is shown in the console.
         - When the user clicks on "Quit", the GUI closes.
         and start the SFTool.
"""

import PySimpleGUI as sg  # pip install PySimpleGUI
import datetime

from SFTool.case import Case
from SFTool.database_helper import insert_data_case_information
from SFTool.database_helper import select_database
from SFTool.sys_specs import register_system_specs_to_database
from SFTool.hashing import get_pathname_and_hashes
from SFTool.compare_hashes import compare_hashes
from SFTool.hashing import convert_md5_to_sha1
from SFTool.network_checker import internet_on
from SFTool.virustotal import register_malware_to_database


# from threading import Thread
# from time import sleep
#
#
# def threaded_function(arg):
#     for i in range(arg):
#         print("running")
#         sleep(1)
#
#
# def thread_main():
#     thread = Thread(target = threaded_function, args = (10, ))
#     thread.start()
#     thread.join()
#     print("thread finished...exiting")

# The function view database shows the database in the console
def view_database():
    select_database()
    return None


# The function scan malware is the main program of the SFTool: SFTool is scanning the system of availability of malware
def scan_malware():
    result = 'OK'
    try:
        print("Malware scan is started" + "\n")

        print('Registrating system specifications... ' + "\n")
        register_system_specs_to_database()  # write system specifications to database

        print('calculating hashes... ' + "\n")
        get_pathname_and_hashes()  # calculate the md5 hashes of files on the system

        # check if the system has an connection to the internet
        if internet_on():
            print('The system has an connection to the internet!' + "\n")
            print('Detecting malware in VirusShare... ' + "\n")
            compare_hashes()  # offline database: virusshare (compare system hashes with the hahses of VirusShare)

            print('Converting MD5 to SHA1' + "\n")
            convert_md5_to_sha1()  # converts the malware md5 hashes to sha1

            print('Checking malware name in VirusTotal... ' + "\n")
            register_malware_to_database()  # online database: VirusTotal (writes the malware information to the
            # database)
        elif not internet_on():
            print('The system has not an connection to the internet!' + "\n")
            print('Detecting malware in VirusShare... ' + "\n")
            compare_hashes()  # offline database: virusshare (compare system hashes with the hahses of VirusShare)

            print('Converting MD5 to SHA1' + "\n")
            convert_md5_to_sha1()  # converts the malware md5 hashes to sha1

        print('Copying malware to USB drive..')
        # copy_malware()  miscchien in de virustotal class

        print('The malware scan is finished!')

    except Exception as e:
        print(e)
        result = e

    return result


def show_window():
    status_mode = sg.Text('Welcome!', size=(30, 1), font=('Arial', 14), text_color='red')
    empty_row = sg.Text('', size=(1, 1))  # creates a empy row for the format of the GUI
    # create buttons
    start_malware = sg.Button('Start malware scan', size=(17, 1), font=('Arial', 18), button_color=('black', 'white'),
                              enable_events=True, )
    view_databasee = sg.Button('View Database', size=(13, 1), font=('Arial', 18), button_color=('black', 'white'))
    quit_startmenu = sg.Button('Quit', size=(5, 1), font=('Arial', 18), button_color=('black', 'white'))

    # Layout the design of the GUI
    layout = [
        [sg.Text('SFTool - Synergy Forensics Triage Tool', size=(31, 2), text_color='blue', font=('Arial', 30))],
        [sg.Text('Case Name:', size=(13, 1), font=('Arial', 14)), sg.InputText(key='_CASE_NAME_', font=('Arial', 14))],
        [sg.Text('Start Number:', size=(13, 1), font=('Arial', 14)),
         sg.InputText(key='_START_NUMBER', font=('Arial', 14))],
        [sg.Text('Investigator:', size=(13, 1), font=('Arial', 14)),
         sg.InputText(key='_INVESTIGATOR_', font=('Arial', 14))],
        [sg.Text('Comment:', size=(13, 1), font=('Arial', 14)), sg.InputText(key='_COMMENT_', font=('Arial', 14))],
        [sg.Text('Status: ', size=(13, 1), font=('Arial', 14)), status_mode],
        [empty_row],
        [empty_row],
        [view_databasee, empty_row, quit_startmenu, empty_row, start_malware],
        [empty_row]
    ]

    window = sg.Window('SFT - Start menu').Layout(layout)  # Show the Window to the user

    while True:
        event, value = window.Read()  # Read the Window
        # Take appropriate action based on button
        if event == 'View Database':
            view_database()

        elif event == 'Start malware scan':
            # start_malware.Update(button_color=('white', 'black'))
            case_name = value['_CASE_NAME_']
            start_number = value['_START_NUMBER']
            investigator_name = value['_INVESTIGATOR_']
            comment = value['_COMMENT_']
            time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            if case_name == '' or start_number == '' or investigator_name == '':
                sg.Popup("Fill in the case data on the start menu. " + "\n" +
                         "Required: case name, start number and investigator's name" + "\n")
                print("Fill in the case data on the start menu. " + "\n" +
                      "Required: case name, start number and investigator's name" + "\n")
            else:
                print("Time: " + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
                print("Event: " + event + "\n" + "\n", "Case Name: " + "\t" + case_name + "\n",
                      "Start Number: " + "\t" +
                      start_number + "\n", "Investigator: " + "\t" + investigator_name + "\n", "Comment: " +
                      "\t" + "\t" + comment + "\n")

                case_data = Case(case_name, start_number, investigator_name, comment, time)
                insert_data_case_information(case_data)  # write case information to database

                result = scan_malware()
                print(result)
                status_mode.Update(result)

        elif event == 'Quit' or event is None:
            window.Close()
            break

    return window


def sftool():
    try:
        print("Creates a memory dump of the system...")
        # memory dump maken hier()
        # live triage hier()
        show_window()
    except Exception as e:
        print(e)


def main():
    sftool()


if __name__ == '__main__':
    main()

