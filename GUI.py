import PySimpleGUI as sg
import datetime


def view_database():
    print("view database")
    return None


def scan_malware():
    print("scan malware")
    sg.PopupOK('SFT is scanning malware')
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

    # Show the Window to the user
    window = sg.Window('SFT - Start menu').Layout(layout)
    # event, values = window.Read()
    # print(event, values['_CASE_NAME_'], values['_START_NUMBER'], values['_INVESTIGATOR_'], values['_COMMENT_'])

    while True:
        # Read the Window
        event, value = window.Read()
        # Take appropriate action based on button
        if event == 'View Database':
            view_database()
        elif event == 'Scan Malware':
            scan_malware()
        elif event == 'Submit':
            timeformat = '%Y-%m-%d-%H-%M-%S'
            print("Time: " + datetime.datetime.now().strftime(timeformat))
            print("Event: " + event + "\n" + "\n", "Case Name: " + "\t" + value['_CASE_NAME_'] + "\n", "Start Number: " + "\t" +
                  value['_START_NUMBER'] + "\n", "Investigator: " + "\t" + value['_INVESTIGATOR_'] + "\n", "Comment: " +
                  "\t" + "\t" + value['_COMMENT_'])
        elif event == 'Quit' or event is None:
            window.Close()
            break

    return window


def main():
    show_window()


if __name__ == '__main__':
    main()
