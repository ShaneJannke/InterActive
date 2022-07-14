from datetime import date
import os
import numpy as np
import pyodbc
from tkinter import Toplevel
from tkinter import StringVar
from tkinter import Radiobutton
from tkinter import Button
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import W
from tkinter import Label
from tkinter import Entry
import Task_Manager

#Change the Status of a TM Request, copied from Sub Log
def TM_Change_Status(Sub_Request_V,Report_Text,Main_Tree,Book):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()

    #if no sub request selected, report that to user
    if ID == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        #get the current status
        Status_EXE = "EXEC Interactive.dbo.TM_Get_Status @id=?"
        c.execute(Status_EXE,ID)
        statusdata = c.fetchall()
        statusarray = np.array(statusdata)
        Status = statusarray[0,0]

        if Status == "Initiated":
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "You may not change the status of initiated requests" + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
        else:
            top = Toplevel()
            top.geometry("400x400")
            top.title('Change Status')

            #tell the user which ID they are changing the status of
            ID_Label = Label(top, text="Request #" + ID)
            ID_Label.pack()

            MODES = [
                    ("Open", "Open"),
                    ("In Progress", "In Progress"),
                    ("Pending Review", "Pending Review"),
                    ('Rejected', 'Rejected'),
                    ("Closed", 'Closed')
                    ]

            _status = StringVar()
            #set the selected status to the current one
            _status.set(Status)

            for text, mode in MODES:
                Radiobutton(top, text = text, variable = _status, value = mode).pack(anchor = W)

            btn = Button(top, text = "Submit", command = lambda: clicked(_status.get()))
            btn.pack()

    def clicked(value):

        _status = str(value)
        conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=Interactive;"
                               "Trusted_Connection=yes;")
        c = conn2.cursor()

        EXE_STRING = "EXEC Interactive.dbo.TM_Change_Status @id=?, @status=?"
        try:
            c.execute(EXE_STRING,ID,_status)
            '''
            6/8/22 SJ
            If selected status is the same as current status, don't update the changelog
            '''
            if Status != _status:
                e1 = "Request " + ID + " status changed to " + _status + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                Task_Manager.TM_Update_Change_Log(e1,Report_Text,ID)  

        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1 + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")        
        c.commit()
        top.destroy()
        top.update()

        Task_Manager.TM_View_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)
        
    return