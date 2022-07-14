import pyodbc
import numpy as np
from datetime import date
import os
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import Toplevel
from tkinter import Label
from tkinter import Entry
from tkinter import Button
import Main_Trees
import Sub_Log_Files
import Task_Manager


def TM_Add_PCBA(Report_Text,Sub_Request_V,Main_Tree,ME_clicked):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=Testdatabase;"
                               "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()

    if ID == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Sub Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:

        top = Toplevel()
        top.geometry("200x200")
        top.title('My Second Window')

        name = Label(top,text = "TM Request #"+ID).pack()

        PCBAe1 = Label(top, text = "PCBA #").pack()
        e1 = Entry(top)
        e1.pack()

        REVe2 = Label(top, text = "Rev").pack()
        e2 = Entry(top)
        e2.pack()

        btn = Button(top, text = "Submit", command = lambda: submit(e1,e2))
        btn.pack()

        def submit(e1,e2):

            PCBA = e1.get()
            Rev = e2.get() 

            try:
                exe_String1 = "EXEC Testdatabase.dbo.TM_Add_PCBA @id=?, @PCBA=?, @PCBA_Rev=?"
                c.execute(exe_String1,ID,PCBA,Rev) 
                Remove_Iniated_2 = "EXEC Testdatabase.dbo.TM_Remove_Initated_ID_2" #This removed all iniated from the log that already have open/closed requests
                c.execute(Remove_Iniated_2)

            except Exception as e:
                e1 = str(e)
                Report_Text.configure(state = NORMAL)
                Report_Text.delete('1.0',END)
                Report_Text.insert(END, e1 + "\n")
                Report_Text.configure(state = DISABLED)
                Report_Text.see("end")

            c.commit()
            c.close()
            top.destroy()
            top.update()

            Main_Trees.Clear_Main_Tree(Main_Tree)
            Task_Manager.TM_populate_resp(Main_Tree,ME_clicked,Report_Text)

        return

    return