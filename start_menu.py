"""
Author: Mariska Temming, S1106242
Summary: The database_helper initialize the database (three tables) and execute queries (insert data into the database)
"""

import PySimpleGUI as sg
import datetime
from SFTool.case import Case
from SFTool.database_helper import insert_data_case_information
from SFTool.database_helper import select_database


def view_database():
    select_database()
    return None


def scan_malware():
    print("scan malware")
    sg.PopupOK('SFT is scanning malware')
    # hier main aanroepen?
    return None


def show_window():
    # Layout the design of the GUI
    layout = [
        [sg.Text('SFT - Synergy Forensic Triage Tool', size=(30, 2), text_color='blue', font=('Arial', 30))],
        [sg.Text('Case Name:', size=(13, 1), font=('Arial', 14)), sg.InputText(key='_CASE_NAME_', font=('Arial', 14))],
        [sg.Text('Start Number:', size=(13, 1), font=('Arial', 14)), sg.InputText(key='_START_NUMBER', font=('Arial', 14))],
        [sg.Text('Investigator:', size=(13, 1), font=('Arial', 14)),
         sg.InputText(key='_INVESTIGATOR_', font=('Arial', 14))],
        [sg.Text('Comment:', size=(13, 1), font=('Arial', 14)), sg.InputText(key='_COMMENT_', font=('Arial', 14))],

        [sg.Button('View Database', size=(11, 4), font=('Arial', 20), pad=(0, 0)),
         sg.Button('Submit', size=(5, 4), font=('Arial', 20), pad=(0, 0)),
         sg.Button('Quit', size=(3, 4), font=('Arial', 20), pad=(0, 0)),
         sg.Button('Scan Malware', size=(11, 4), font=('Arial', 20), pad=(0, 0))]
    ]

    window = sg.Window('SFT - Start menu').Layout(layout)   # Show the Window to the user

    while True:
        event, value = window.Read()    # Read the Window
        # Take appropriate action based on button
        if event == 'View Database':
            view_database()
        elif event == 'Scan Malware':
            scan_malware()
        elif event == 'Submit':
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
        elif event == 'Quit' or event is None:
            window.Close()
            break

    return window


def main():
    show_window()


if __name__ == '__main__':
    main()
