import pyodbc
import os
from datetime import date
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import Toplevel
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import StringVar
from tkinter import Radiobutton
from tkinter import W
import Sub_Log_Files

#removed book as it was not used
def Sub_Add_Alt(Main_Tree,Sub_Options_V,Sub_Request_V,Report_Text,Sub_clicked,Book):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor() 
    ID = Sub_Request_V.get()

    #if no sub request selected, report that to user
    if ID == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Sub Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        top = Toplevel()
        top.geometry("300x300")
        top.title('Add Alternate')

        name = Label(top,text = "Sub Request #"+ID).pack()

        WOe1 = Label(top, text = "Old Part Number").pack()
        e1 = Entry(top)
        e1.pack()
        PNe2 = Label(top, text = "Alt Part Number").pack()
        e2 = Entry(top)
        e2.pack()
        PCBAe3 = Label(top, text= "PCBA Number").pack()
        e3 = Entry(top)
        e3.pack() 

        '''
        6/16/22 SJ
        Added radio buttons to allow for different alternate PN options
        '''
        MODES = [
        ("Alt PN", "Alt PN"),
        ("Broker", "Broker"),
        ("Consigned", "Consigned")
        ]

        _status = StringVar()
        #set the selected option
        _status.set('Alt PN')

        for text, mode in MODES:
            Radiobutton(top, text = text, variable = _status, value = mode).pack(anchor = W)

        btn = Button(top, text = "Submit", command = lambda: sub_submit(e1.get(),e2.get(),_status.get(),e3.get())) #6/16/22 SJ - added the radio button result as a variable to pass
        btn.pack(pady=10)

    def sub_submit(e1,e2,value,e3): #6/16/22 SJ - added the radio button value as a passed variable

        PN = e1
        ALT = e2
        PCBA = e3

        EXE_STRING = "EXEC Interactive.dbo.SUB_Add_Alt @id=?, @ipn=?, @alt=?, @Type=?, @PCBA=?" #6/16/22 SJ - added @Type as a SQL check for the radio button choice
        try:    
            c.execute(EXE_STRING,ID,PN,ALT,value,PCBA) #6/16/22 SJ - passing radio button value as the Type in SQL stsatement
            if value == 'Alt PN': #6/16/22 SJ - if value is Alt PN, add the pn to changelog
                e1 = "Alternate PN " + ALT + " added to Sub Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
            else: #6/16/22 SSJ - if value is not Alt PN, insert the chosen value to changelog
                e1 = "Alternate PN " + value + " added to Sub Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
            Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID)    
        except Exception as e:
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1 + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
             
        c.commit()
        c.close()
        top.destroy()
        top.update()

        Sub_Log_Files.View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)
    return