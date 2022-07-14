import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED

def Update_Sub_Change_Log(e1,Report_Text,ID):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()

    #get the current changelog from database
    EXE_STRING_GETLOG = "EXEC Interactive.dbo.SUB_Get_Log @id=?"        

    try:
        c.execute(EXE_STRING_GETLOG,ID)
        data = c.fetchall()
        np_data = np.array(data)
        note = str(np_data[0])

        if note == '[None]':
            note = note[1:-1]
        else:
            note = note[2:-2]
        note = note.replace(r'\n','\n')

        #if note is none, enter the user's note
        if note == 'None':
            NOTE = e1
        else:
            #if note exists already, add requested note onto previous note
            NOTE = note + "\n" + e1
    
        try:
            #update the change log with new changes
            EXE_STRING = "EXEC Interactive.dbo.SUB_Change_Log @id=?, @note=?"
            c.execute(EXE_STRING,ID,NOTE)  
        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1 + "\n")
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