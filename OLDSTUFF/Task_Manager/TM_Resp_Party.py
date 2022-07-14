import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import ttk
import Task_Manager

#set responsible party to user selected from the dropdown
def Set_Resp_Party(clicked,Sub_Request_V,Main_Tree,Book,frame6,Report_Text):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Testdatabase;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    #get the name of the selected user from the dropdown
    USER = clicked.get()
    WO = Sub_Request_V.get()

    if WO == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Work Order Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        try:
            EXE_STRING = "EXEC Testdatabase.dbo.TM_Set_Resp_Party @USER=?, @WO=?"
            c.execute(EXE_STRING,USER,WO)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "Responsible Party for WO " + WO + " set to " + USER + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
            c.commit()
            c.close()
        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1 + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
    return
