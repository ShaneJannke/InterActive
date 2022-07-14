import pyodbc
import numpy as np
import os
from datetime import date
from tkinter import simpledialog
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import END
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Toplevel
import Sub_Log_Files

#removed book, sub_options_v as it was not used
def Sub_Add_PO(Sub_Request_V,Report_Text,Main_Tree,Book):
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
        Status_EXE = "EXEC Interactive.dbo.SUB_Get_Status @id=?"
        c.execute(Status_EXE,ID)
        statusdata = c.fetchall()
        statusarray = np.array(statusdata)
        status = statusarray[0,0]
        if status != "PO Needed":
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "This button can only be used for Sub Requests in PO Needed" + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
        else:
            top = Toplevel()
            top.geometry("250x200")
            top.title('Add PO#')

            name = Label(top,text = "Sub Request #"+ID).pack()

            PNe1 = Label(top, text = "Alternate PN").pack()
            e1 = Entry(top)
            e1.pack()    
            POe2 = Label(top, text = "Part PO#").pack()
            e2 = Entry(top)
            e2.pack()
            Datee3 = Label(top, text = "PO# Due Date (dd/mm/yyyy)").pack()
            e3 = Entry(top)
            e3.pack()

            btn = Button(top, text = "Submit", command = lambda: sub_submit(e1,e2,e3))
            btn.pack()

        def sub_submit(e1,e2,e3):

            PN = e1.get()
            PONO = e2.get()
            PO_DATE = e3.get()

            EXE_STRING = "EXEC Interactive.dbo.SUB_Add_PO @pn=?, @id=?, @po=?, @po_date=?"
            try:    
                c.execute(EXE_STRING,PN,ID,PONO,PO_DATE)

                e1 = "PO " + PONO + " added to Sub Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
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



