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
import Task_Manager

#Add an Assembly to a Request, copied mostly from Add By WONO from Sub Log
def TM_Add_Assembly(Report_Text,Sub_Request_V,Main_Tree,Book):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=Interactive;"
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
        top.geometry("300x250")
        top.title('Add Assembly')

        name = Label(top,text = "TM Request #"+ID).pack()

        PCBAe1 = Label(top, text = "PCBA #").pack()
        e1 = Entry(top)
        e1.pack()

        REVe2 = Label(top, text = "REV").pack()
        e2 = Entry(top)
        e2.pack()

        CustDatee3 = Label(top, text = "Binder Date").pack()
        e3 = Entry(top)
        e3.pack()

        btn = Button(top, text = "Submit", command = lambda: sub_submit(e1,e2,e3))
        btn.pack()

        def sub_submit(e1,e2,e3):

            PCBA = e1.get()
            REV = e2.get()
            CustDate = e3.get()
            
            try:
                exe_String1 = "EXEC Interactive.dbo.TM_Add_Assembly @id=?, @pcba=?, @rev=?, @custdate=?"
                c.execute(exe_String1,ID,PCBA,REV,CustDate) 
                Remove_Iniated_2 = "EXEC Interactive.dbo.TM_Remove_Initated_ID_2" #This removed all iniated from the log that already have open/closed requests
                c.execute(Remove_Iniated_2)

                e1 = "Assembly " + PCBA + " Rev " + REV + " added to Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                Task_Manager.TM_Update_Change_Log(e1,Report_Text,ID)

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
            Task_Manager.TM_View_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)

        return

    return