import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import Frame
from tkinter import Canvas
from tkinter import Label
from tkinter import Tk
from tkinter import BOTH
from tkinter import TOP
from tkinter import HORIZONTAL
from tkinter import BOTTOM
from tkinter import X
from tkinter import W
from tkinter import ttk

def TM_Feedback(Sub_Request_V, Report_Text, root):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Testdatabase;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    WO = Sub_Request_V.get()

    #app_width = 1200
    #app_height = 500

    #screen_width = root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()

    #app_width_loc = int(screen_width/2 - app_width/2)
    #app_height_loc = int(screen_height/2 - app_height/2)

    #if no WO selected, return error
    if WO == 'None':

        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Work Order Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        EXE_STRING = "EXEC Testdatabase.dbo.TM_Prod_Feedback @PCBA=?"
        c.execute(EXE_STRING,WO)
        data = c.fetchall()
        np_data = np.array(data)
        feedback = str(np_data[0])
        feedback = feedback[2:-2]

        feedback = feedback.replace(r'\n','\n')
        feedback = feedback.replace(r'\t','\t')
        feedback = feedback.replace(r'\r','\r')

        if feedback == "":
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "No Feedback Found" + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")

        else:
        #TopLevel = Tk()    
        #TopLevel.title('Production Feedback')
        #TopLevel.iconbitmap('S:\\_ENG_MANUFACTURING\\Applications\\Inter-Active\\Launcher\\Icon.ico')
        #TopLevel.geometry(f'{app_width}x{app_height}+{app_width_loc}+{app_height_loc}')

        #Create a Main Frame
        #main_frame = Frame(TopLevel)
        #main_frame.pack(fill=BOTH, expand=1)

        #Create a canvas
        #my_canvas = Canvas(main_frame)
        #my_canvas.pack(side=TOP, fill=BOTH, expand=1)

        #Add a scrollbar to the canvas
        #my_scrollbar = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
        #my_scrollbar.pack(side=BOTTOM, fill=X)

        #configure the canvas
        #my_canvas.configure(xscrollcommand=my_scrollbar.set)
        #my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        #Create another frame inside the canvas
        #second_frame = Frame(my_canvas)

        #add that new frame to a window in the canvas
        #my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        #print the feedback on several lines
        #for index, x in enumerate(data):
         #   num = 0
          #  index += 2
           # for y in x:
            #    feedback_label = Label(second_frame, text=y)
             #   feedback_label.grid(row=index, column=num+1, sticky=W)
              #  num +=1 

        #WO_label = Label(second_frame, text="WO#" + WO + " Feedback")
        #WO_label.grid(row=0, column=1, padx=10, pady=10)

            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, feedback + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
    return

