import numpy as np
import pyodbc
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees
import Sub_Log_Files

def Sub_Remove_Request(Sub_Request_V,Report_Text,Main_Tree,Sub_Options_V,Sub_clicked):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                       "Server=DC01;"
                       "Database=Interactive;"
                       "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()

    EXE_STRING ="EXEC Interactive.dbo.SUB_Remove_Request @ID=?, @status=?"
    
    #if no sub request selected, report that to user
    if ID == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, "No Sub Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        Status_EXE = "EXEC Interactive.dbo.SUB_Get_Status @id=?"
        c.execute(Status_EXE,ID)
        statusdata = c.fetchall()
        statusarray = np.array(statusdata)
        status = statusarray[0,0]

        #dont allow the user to delete requests that arent open
        if status == "Closed":
            Report_Text.configure(state = NORMAL)
            Report_Text.insert(END, "You can not delete closed requests" + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
        else:
            #Trap error if raised
            try:        
                c.execute(EXE_STRING,ID,status)      
            except Exception as e:
                #messagebox.showinfo("Results",e)
                e1 = str(e)
                Report_Text.configure(state = NORMAL)
                Report_Text.insert(END, e1 + "\n")
                Report_Text.configure(state = DISABLED)
                Report_Text.see("end")
                 
            c.commit()
            c.close()
            
        Sub_Request_V.set(None)

        Main_Trees.Clear_Main_Tree(Main_Tree)
        Sub_Log_Files.sub_request_populate(Main_Tree,Sub_Options_V,Report_Text,Sub_clicked)
    
    return