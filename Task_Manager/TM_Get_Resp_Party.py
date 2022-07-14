import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import ttk

#get the responsibe party from a TM Request, copied code from Sub Log
def TM_Get_Resp_Party(Sub_Request_V,Report_Text):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()

    if ID == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        try:
            EXE_STRING = "EXEC Interactive.dbo.TM_Get_Resp_Party @id=?"
            c.execute(EXE_STRING,ID)

            data = c.fetchall()
            respparty = np.array(data)
            user = []

            rowcount = 0
            for row in respparty:
                user.append(respparty[rowcount,0])
                rowcount += 1
            if user[0] == None:
                Report_Text.configure(state = NORMAL)
                Report_Text.delete('1.0',END)
                Report_Text.insert(END, "No Responsible Party for Request " + ID + "\n")
                Report_Text.configure(state = DISABLED)
                Report_Text.see("end")
            else:
                party = user[0].strip()
                Report_Text.configure(state = NORMAL)
                Report_Text.delete('1.0',END)
                Report_Text.insert(END, "Responsible Party for Request " + ID + " is " + party + "\n")
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