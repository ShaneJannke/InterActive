import pyodbc
import numpy as np
from tkinter import Toplevel
from tkinter import Label
from tkinter import Text
from tkinter import WORD
from tkinter import END
from tkinter import Button
from tkinter import messagebox
from tkinter import DISABLED
from tkinter import NORMAL 
import Main_Trees
import Sub_Log_Files

def Sub_Request_Note(Sub_Request_V,Report_Text,Main_Tree,Book):

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

            top = Toplevel()
            top.geometry("600x250")
            top.title('Add Notes')
            
            name = Label(top,text = "Request # " + ID + " Note ")
            name.pack()

            e1 = Text(top, width = 60, height = 10, wrap = WORD)
            e1.pack()

            btn = Button(top, text = "Submit", command = lambda: sub_submit(e1.get("1.0",'end-1c'),ID))
            btn.pack()  
        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1 + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")        
    

    def sub_submit(e1,ID):
        #if no notes entered, replace "None" with the requested note
        if note == 'None':
            NOTE = e1
        else:
        #if note exists already, add requested note ontop of previous note
            NOTE = note + "\n" + e1
            
        try:
            EXE_STRING = "EXEC Interactive.dbo.SUB_Request_Note @id=?, @note=?"
            c.execute(EXE_STRING,ID,NOTE)  
        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1)
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")        
        c.commit()
        c.close()
        top.destroy()
        top.update()

        Main_Trees.Clear_Main_Tree(Main_Tree)
        Sub_Log_Files.View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)
        return


    return