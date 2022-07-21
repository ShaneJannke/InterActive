import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees

#code mostly copied from Sub Log
def TM_Update_Feedback():

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                       "Server=DC01;"
                       "Database=Interactive;"
                       "Trusted_Connection=yes;")
    c = conn2.cursor()

    #Trap error if raised
    try:

        #Update the feedback display incase feedback has been added or removed
        c.execute('EXEC Interactive.dbo.Update_TM_Feedback')
        
    except Exception as e:
        #messagebox.showinfo("Results",e)
        e1 = str(e)
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, e1 + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
             
    c.commit()
    c.close()

    return 