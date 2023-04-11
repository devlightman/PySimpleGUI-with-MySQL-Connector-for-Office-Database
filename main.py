import PySimpleGUI as sg
import mysql.connector

# MySQL Connection

dbms = mysql.connector.connect( host='127.0.0.1', 
                                user='', # Your Username
                                password='', #Your Password
                                database='') #Database Name

myCursor = dbms.cursor()

# Add some color to the window
sg.theme('Default1')
sg.set_options(font='Courier 16')

RecordsData = []
myCursor.execute("SELECT * FROM medivet.inputs")
for i in myCursor:
    RecordsData.append(list(i))
headersRecords = ['pay_to', 'amount_words', 'amount', 'address', 'purpose', 'drawer', 'issue_date', 'company']

# Functions to update new data on the display tables on refreshing

def refresh_records():
    dbms2 = mysql.connector.connect(host="127.0.0.1",
                                    user='', # Your Username
                                    password='', #Your Password
                                    database='') #Database Name

    myCursor2 = dbms2.cursor()
    data = []
    myCursor2.execute("SELECT * FROM medivet.inputs;")
    for j in myCursor2:
        data.append(list(j))
    window1['-table1-'].Update(values=data)
    sg.popup("Records Updated!")

# Clearing from functions

def clear_records():
    for key in values:
        window1['pay_to'].update('')
        window1['amount_words'].update('')
        window1['amount'].update('')
        window1['address'].update('')
        window1['purpose'].update('')
        window1['drawer'].update('')
        window1['issue_date'].update('')
        window1['company'].update('')

    return None

# Submitting functions

def submit_records():
    pay_to = values['pay_to']
    if pay_to == '':
        sg.popup_error('Missing Pay_to')
    amount_words = values['amount_words']
    if amount_words == '':
        sg.popup_error('Missing amount in words')
    amount = values['amount']
    if amount == '':
        sg.popup_error('Missing amount')
    address = values['address']
    if address == '':
        sg.popup_error('Missing address')
    purpose = values['purpose']
    if purpose == '':
        sg.popup_error('Missing purpose')
    drawer = values['drawer']
    if drawer == '':
        sg.popup_error('Missing drawer')
    issue_date = values['issue_date']
    if issue_date == '':
        sg.popup_error('Missing issue_date')
    company = values['company']
    if company == '':
        sg.popup_error('Missing company')
    else:
        try:
            command = myCursor.execute("""INSERT INTO medivet.inputs (pay_to, amount_words, amount, address, purpose, drawer, issue_date, company) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",(pay_to, amount_words, amount, address, purpose, drawer, issue_date, company))
            print(command)
            myCursor.execute(command)
            dbms.commit()
            choice = sg.popup_ok_cancel("Please confirm entry")
            if choice == 'OK':
                clear_records()
                sg.popup_quick('records entered')
            else:
                sg.popup_ok('Edit Entry')
        except:
            sg.popup('Please check your inputs. Something is wrong!')

# GUI Layout

recordsTable_layout = [
    [sg.T('RECORDS')],
    [sg.Table(headings=headersRecords, values=RecordsData, display_row_numbers=True, enable_events=True,
            justification='center', key='-table1-')],
    [sg.Button("Refresh Records", key='-refreshR-', expand_x=True)],
    [sg.Button("Exit", expand_x=True)]
]

RecordsForm_layout = [
    [sg.T('Records File')],
    [sg.T('pay_to'), sg.Push(), sg.I(size=(30, 5), key='pay_to')],
    [sg.T('amount_words'), sg.Push(), sg.I(size=(30, 5), key='amount_words')],
    [sg.T('amount'), sg.Push(), sg.I(size=(30, 5), key='amount')],
    [sg.T('address'), sg.Push(), sg.I(size=(30, 5), key='address')],
    [sg.T('purpose'), sg.Push(), sg.I(size=(30, 5), key='purpose')],
    [sg.T('drawer'), sg.Push(), sg.I(size=(30, 5), key='drawer')],
    [sg.T('issue_date'), sg.Push(), sg.I(size=(30, 5), key='issue_date')],
    [sg.T('company'), sg.Push(), sg.Combo(size=(30, 5), values=['Medivet', 'Agri-Master'], key='company')],
    [sg.Button('Submit', key='-submit-', expand_x=True), sg.Button('Clear', key='-clear-', expand_x=True), sg.Button('Exit', key='-exit-', expand_x=True)]
]

main_layout = [
    [sg.Button('View RECORDS', key='-viewR-')],
    [sg.Button('Enter RECORDS', key='-enterR-')],
    [sg.Button('Exit', key='-exit-')]
]
window= sg.Window("Medivet Check", main_layout)

# MAIN

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED or '-exit-'):
        break
    if event == '-viewR-':
        window1 = sg.Window("", recordsTable_layout)
        event, values = window1.read()
        if event == 'Exit':
            window1.close()
        if event == '-refreshR-':
            refresh_records()
    if event == '-enterR-':
        window1 = sg.Window("Records Form", RecordsForm_layout)
        event, values = window1.read()
        if event == '-submit-':
            submit_records()
        if event == '-clear-':
            clear_records()
        if event == '-exit-':
            window1.close()

window.close()
        
