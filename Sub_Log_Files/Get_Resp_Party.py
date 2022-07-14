import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import ttk

#get responsible party for selected Sub Request
def Get_Resp_Party(Sub_Request_V,Report_Text):

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
        try:
            #get stored responsible SC from database per selected Sub Request ID
            SC_EXE_STRING = "EXEC Interactive.dbo.SUB_Get_Resp_SC @ID=?"
            c.execute(SC_EXE_STRING,ID)
            #format the data to remove brackets and quotes
            SC_data = c.fetchall()
            respSC = np.array(SC_data)
            SC = respSC[0,0]
            #display the responsible Supply Chain in the report text
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "Responsible Supply Chain for Request " + ID + " is " + SC + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")

            #get stored responsible ME from database per selected Sub Request ID
            ME_EXE_STRING = "EXEC Interactive.dbo.SUB_Get_Resp_ME @ID=?"
            c.execute(ME_EXE_STRING,ID)
            #format the data to remove brackets and quotes
            ME_data = c.fetchall()
            respME = np.array(ME_data)
            ME = respME[0,0]
            #display the responsible ME in the report text
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "Responsible MFG Engineering for Request " + ID + " is " + ME + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")

            #get stored responsible CAS from database per selected Sub Request ID
            CAS_EXE_STRING = "EXEC Interactive.dbo.SUB_Get_Resp_CAS @ID=?"
            c.execute(CAS_EXE_STRING,ID)
            #format the data to remove brackets and quotes
            CAS_data = c.fetchall()
            respCAS = np.array(CAS_data)
            CAS = respCAS[0,0]
            #display the responsible CAS in the report text
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "Responsible CAS for Request " + ID + " is " + CAS + "\n")
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