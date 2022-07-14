import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import ttk

def TM_View_Note(Sub_Request_V, Report_Text):
    
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Testdatabase;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    WO = Sub_Request_V.get()

    #if no WO selected, return error
    if WO == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Work Order Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")

    else:
        EXE_STRING = "EXEC Testdatabase.dbo.TM_View_Note @WO=?"

        try:
            c.execute(EXE_STRING,WO)
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
            Report_Text.insert(END, "WO " + WO + " Note:\n" + note + "\n")
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