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
import Sub_Log_Files
def Sub_Change_QTY_Needed(Report_Text,Sub_Request_V,Main_Tree,Sub_Options_V,Sub_clicked,Book):

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
        top.geometry("200x200")
        top.title('Change QTY Needed')

        name = Label(top,text = "Sub Request #"+ID).pack()

        QTYe1 = Label(top, text = "QTY Needed").pack()
        e1 = Entry(top)
        e1.pack()

        WOe2 = Label(top, text = "Work Order #").pack()
        e2 = Entry(top)
        e2.pack()

        PNe3 = Label(top, text = "Part Number").pack()
        e3 = Entry(top)
        e3.pack()

        btn = Button(top, text = "Submit", command = lambda: sub_submit(e1,e2,e3))
        btn.pack()

    def sub_submit(e1,e2,e3):

        QTY = e1.get()
        WO = e2.get()
        PN = e3.get()

        try:
            '''
            6/9/22 SJ
            This will override the current QTY needed and replace it with the entered value
            '''
            SET_QTY_STRING = "EXEC Interactive.dbo.SUB_Set_QTY_Needed @ID=?, @QTY=?, @iWO=?, @iPN=?"
            c.execute(SET_QTY_STRING,ID,QTY,WO,PN)

            if WO == '':
                e1 = "Sub Request " + ID + " Quantity Needed updated to " + QTY + " for PN " + PN + " and Work Order: None by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID) 
            else:
                e1 = "Sub Request " + ID + " Quantity Needed updated to " + QTY + " for PN " + PN + " and Work Order " + WO + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID) 

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

        Sub_Log_Files.View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)

        return

    return