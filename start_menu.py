"""
Author: Mariska Temming, S1106242
Summary: This startmenu shows the user interface of the SFTool and start the SFTool. 
"""

import PySimpleGUI as sg
import datetime
from SFTool.case import Case
from SFTool.database_helper import insert_data_case_information
from SFTool.database_helper import select_database

from SFTool.sys_specs import register_system_specs_to_database
from SFTool.hashing import get_pathname_and_hashes
from SFTool.virustotal import register_malware_to_database


def view_database():
    select_database()
    return None


def scan_malware():
    result = 'OK'
    try:
        print("Malware scan is started")

        register_system_specs_to_database()     # write system specifications to database
        print('Registrating system specifications... ')

        get_pathname_and_hashes()
        print('calculating hashes... ')

        # virusshare()  # virusshare script aanroepen
        print('Detecting malware in VirusShare... ')

        register_malware_to_database()  # virustotal script aanroepen
        print('Checking malware name in VirusTotal... ')

        # kopie malware()
        print('Coping malware to USB drive..')

        print('The malware scan is finished!')

    except Exception as e:
        print(e)
        result = e

    return result


def show_window():
    status_mode = sg.Text('...', size=(20, 1), font=('Arial', 14), text_color='red')
    # create buttons
    start_malware = sg.Button('Start malware scan', size=(15, 4), font=('Arial', 20), pad=(0, 0))
    view_databasee = sg.Button('View Database', size=(11, 4), font=('Arial', 20), pad=(0, 0))
    quit_startmenu = sg.Button('Quit', size=(3, 4), font=('Arial', 20), pad=(0, 0))

    # Layout the design of the GUI
    layout = [
        [sg.Text('SFTool - Synergy Forensics Triage Tool', size=(31, 2), text_color='blue', font=('Arial', 30))],
        [sg.Text('Case Name:', size=(13, 1), font=('Arial', 14)), sg.InputText(key='_CASE_NAME_', font=('Arial', 14))],
        [sg.Text('Start Number:', size=(13, 1), font=('Arial', 14)), sg.InputText(key='_START_NUMBER', font=('Arial', 14))],
        [sg.Text('Investigator:', size=(13, 1), font=('Arial', 14)),
         sg.InputText(key='_INVESTIGATOR_', font=('Arial', 14))],
        [sg.Text('Comment:', size=(13, 1), font=('Arial', 14)), sg.InputText(key='_COMMENT_', font=('Arial', 14))],
        [sg.Text('Status: ', size=(13, 1), font=('Arial', 14)), status_mode],
        [view_databasee, quit_startmenu, start_malware]
    ]

    window = sg.Window('SFT - Start menu').Layout(layout)   # Show the Window to the user

    while True:
        event, value = window.Read()    # Read the Window
        # Take appropriate action based on button
        if event == 'View Database':
            # start_malware.Update(button_color='red')

            view_database()

        elif event == 'Start malware scan':
            # start_malware.Update(button_color='blue')

            case_name = value['_CASE_NAME_']
            start_number = value['_START_NUMBER']
            investigator_name = value['_INVESTIGATOR_']
            comment = value['_COMMENT_']
            time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            print("Time: " + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            print("Event: " + event + "\n" + "\n", "Case Name: " + "\t" + case_name + "\n", "Start Number: " + "\t" +
                  start_number + "\n", "Investigator: " + "\t" + investigator_name + "\n", "Comment: " +
                  "\t" + "\t" + comment)

            case_data = Case(case_name, start_number, investigator_name, comment, time)
            insert_data_case_information(case_data)     # write case information to database

            result = scan_malware()
            print(result)
            status_mode.Update(result)

        elif event == 'Quit' or event is None:
            window.Close()
            break

    return window


def sftool():
    # memory dump maken hier
    # live triage hier
    # if live triage is finished then show window
    show_window()


def main():
    sftool()


if __name__ == '__main__':
    main()
