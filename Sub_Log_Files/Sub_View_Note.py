import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Sub_Log_Files

#6/13/22 SJ - Removed Main_Tree and Book as they were not used
def Sub_View_Note(Sub_Request_V,Report_Text):
    
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()
    
    EXE_STRING = "EXEC Interactive.dbo.SUB_View_Note @id=?"
    
    #if no sub request selected, report that to user
    if ID == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Sub Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        try:
            c.execute(EXE_STRING,ID)
            data = c.fetchall()
            np_data = np.array(data)
            note = str(np_data[0])

            if note == '[None]':
                note = note[1:-1]
            else:
                note = note[2:-2]
            note = note.replace(r'\n','\n')
            note = note.replace(r'\t','\t')

            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "Sub Request " + ID + " Note:\n" + note + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
            
        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1 + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
             
    c.commit()
    c.close()

    return