import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import Toplevel
from tkinter import Label
from tkinter import Button
from tkinter import Text
from tkinter import WORD
from tkinter import ttk

def TM_Request_Note(Sub_Request_V, Report_Text, root):

    app_width = 600
    app_height = 250

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    app_width_loc = int(screen_width/2 - app_width/2)
    app_height_loc = int(screen_height/2 - app_height/2)

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Testdatabase;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    WO = Sub_Request_V.get()

    EXE_STRING = "EXEC Testdatabase.dbo.TM_View_Note @WO=?"

    #if no WO selected, return error
    if WO == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Work Order Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")

    else:
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

            top = Toplevel()
            top.geometry(f'{app_width}x{app_height}+{app_width_loc}+{app_height_loc}')
            top.title('My Second Window')
        
            name = Label(top,text = "Work Order # " + WO + " Note ")
            name.pack()

            #e1 = Text(top, width = 60, height = 10, wrap = WORD, spacing3 = 10)
            e1 = Text(top, width = 60, height = 10, wrap = WORD)
            e1.pack()
            e1.insert(END, note)

            btn = Button(top, text = "Submit", command = lambda: sub_submit(e1.get("1.0",'end-1c'),WO))
            btn.pack()

            def sub_submit(e1,WO):
                #if no notes entered, replace "None" with the requested note
                #if note == 'None':
                NOTE = e1
                #else:
                #if note exists already, add requested note ontop of previous note
                #    NOTE = note + "\n" + e1

                try:
                    EXE_STRING = "EXEC Testdatabase.dbo.TM_Request_Note @WO=?, @note=?"
                    c.execute(EXE_STRING,WO,NOTE)  
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

                return

        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1 + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
    return 