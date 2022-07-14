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
import Sub_Log_Files

#removed sub_options_V as it was not used
def Sub_Change_Status(Sub_Request_V,Report_Text,Main_Tree,Book):

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
        Report_Text.insert(END, "No Sub Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        #get the current status
        Status_EXE = "EXEC Interactive.dbo.SUB_Get_Status @id=?"
        c.execute(Status_EXE,ID)
        statusdata = c.fetchall()
        statusarray = np.array(statusdata)
        Status = statusarray[0,0]
        '''
        6/8/22 SJ
        Get the WONO from database, if Sub Request does not have WONO attached, bypass asking for WONO
        '''
        WO_exe_String = "EXEC Interactive.dbo.SUB_Get_WONO @id=?"
        c.execute(WO_exe_String,ID)
        WOdata = c.fetchall()
        WONOarray = np.array(WOdata)
        WONO = WONOarray[0,0]

        if Status == "Initiated":
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "You may not change the status of initiated or closed requests" + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
        else:
            if WONO == None:
                top = Toplevel()
                top.geometry("400x400")
                top.title('Change Status')

                #tell the user which ID they are changing the status of
                ID_Label = Label(top, text="Sub Request #" + ID)
                ID_Label.pack()

                MODES = [
                        ("Pending SC", "Pending SC"),
                        ("Pending ME", "Pending ME"),
                        ("Pending CAS", "Pending CAS"),
                        ("Pending Customer", "Pending Customer"),
                        ("Customer Responded", "Customer Responded"),
                        ("PO Needed", "PO Needed"),
                        ("Closed", 'Closed')
                        ]

                _status = StringVar()
                #set the selected status to the current one
                _status.set(Status)

                for text, mode in MODES:
                    Radiobutton(top, text = text, variable = _status, value = mode).pack(anchor = W)

                PNe2 = Label(top, text = "Part Number").pack()
                e2 = Entry(top)
                e2.pack()

                btn = Button(top, text = "Submit", command = lambda: clicked2(_status.get(),e2))
                btn.pack()
            else: 
                top = Toplevel()
                top.geometry("400x400")
                top.title('My Second Window')

                #tell the user which ID they are changing the status of
                ID_Label = Label(top, text="Sub Request #" + ID)
                ID_Label.pack()

                MODES = [
                        ("Pending SC", "Pending SC"),
                        ("Pending ME", "Pending ME"),
                        ("Pending CAS", "Pending CAS"),
                        ("Pending Customer", "Pending Customer"),
                        ("Customer Responded", "Customer Responded"),
                        ("PO Needed", "PO Needed"),
                        ("Closed", 'Closed')
                        ]

                _status = StringVar()
                #set the selected status to the current one
                _status.set(Status)

                for text, mode in MODES:
                    Radiobutton(top, text = text, variable = _status, value = mode).pack(anchor = W)

                WOe1 = Label(top, text = "Work Order #").pack()
                e1 = Entry(top)
                e1.pack()

                PNe2 = Label(top, text = "Part Number").pack()
                e2 = Entry(top)
                e2.pack()

                btn = Button(top, text = "Submit", command = lambda: clicked1(_status.get(),e1,e2))
                btn.pack()

    '''
    6/9/22 SJ
    If Sub Request has a WONO attached, run this function when submit is pressed
    '''
    def clicked1(value,e1,e2):

        _status = str(value)
        conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=Interactive;"
                               "Trusted_Connection=yes;")
        c = conn2.cursor()

        WO = e1.get()
        PN = e2.get()

        '''
        6/8/22 SJ
        Change the status based on inputted PN and WONO
        '''
        EXE_STRING = "EXEC Interactive.dbo.Sub_Change_Status_WONO @id=?, @_status=?, @iPN=?, @iWO=?"
        try:
            c.execute(EXE_STRING,ID,_status,PN,WO)
            '''
            6/8/22 SJ
            If selected status is the same as current status, don't update the changelog
            '''
            if Status != _status:
                e1 = "Sub Request " + ID + " For Part Number " + PN + " and Work Order " + WO + " status changed to " + _status + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID)  

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

        Sub_Log_Files.View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)

    '''
    6/9/22 SJ
    If Sub Request does NOT have a WONO attached, run this function when submit is pressed
    '''
    def clicked2(value,e2):

        _status = str(value)
        conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=Interactive;"
                               "Trusted_Connection=yes;")
        c = conn2.cursor()

        PN = e2.get()

        '''
        6/8/22 SJ
        Change the status based on inputted PN
        '''
        EXE_STRING = "EXEC Interactive.dbo.Sub_Change_Status_NO_WONO @id=?, @_status=?, @iPN=?"
        try:
            c.execute(EXE_STRING,ID,_status,PN)
            '''
            6/8/22 SJ
            If selected status is the same as current status, don't update the changelog
            '''
            if Status != _status:
                e1 = "Sub Request " + ID + " For Part Number " + PN + " status changed to " + _status + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID)  

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

        Sub_Log_Files.View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)
        
    return