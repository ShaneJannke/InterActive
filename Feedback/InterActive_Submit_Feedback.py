import pyodbc
import numpy as np
from tkinter import Toplevel
from tkinter import Label
from tkinter import Text
from tkinter import WORD
from tkinter import END
from tkinter import Button
from tkinter import DISABLED
from tkinter import NORMAL 

'''
6/9/22 SJ
Code mostly coppied from Sub Request Note, allows user to enter notes/feedback for interactive.
Created a new table named Feedback since feedback is not tied to a specific part of interactive, must insert a NULL entry upon creation
'''
def Submit_Feedback(Report_Text):

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

        top = Toplevel()
        top.geometry("600x250")
        top.title('InterActive Feedback')
        
        name = Label(top,text = "Enter Your Feedback or Suggestions")
        name.pack()

        e1 = Text(top, width = 60, height = 10, wrap = WORD)
        e1.pack()

        btn = Button(top, text = "Submit", command = lambda: sub_submit(e1.get("1.0",'end-1c')))
        btn.pack()  
    except Exception as e:
        e1 = str(e)
        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, e1 + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")        
    

    def sub_submit(e1):
        #if no notes entered, replace "None" with the requested note
        if note == 'None':
            NOTE = e1
        else:
        #if note exists already, add requested note ontop of previous note
            NOTE = note + "\n" + e1
            
        try:
            EXE_STRING = "EXEC Interactive.dbo.Submit_Feedback @note=?"
            c.execute(EXE_STRING,NOTE)  
        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.insert(END, e1)
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")        
        c.commit()
        c.close()
        top.destroy()
        top.update()

        return


    return