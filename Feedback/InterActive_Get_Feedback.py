import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED

'''
Code mostly coppied from Sub View Note, allows user to view notes/feedback for interactive.
Created a new table named Feedback since feedback is not tied to a specific part of interactive, must insert a NULL entry upon creation
'''

def Get_Feedback(Report_Text):
    
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()

    EXE_STRING = "EXEC Interactive.dbo.View_Feedback"

    try:
        c.execute(EXE_STRING)
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
        Report_Text.insert(END, "Current Feedback:\n" + note + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
        
    except Exception as e:
        e1 = str(e)
        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, e1 + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
             
    c.commit()
    c.close()

    return