import os
from datetime import date
import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import DISABLED
from tkinter import END
from tkinter import ttk
from tkinter import Toplevel
from tkinter import Button
from tkinter import Label
from tkinter import StringVar
from tkinter import OptionMenu
import Task_Manager

#get the selected name from ME dropdown and insert it as the responsible party for selected TM Request
#same code as Sub Log but with less drop downs
def TM_Set_Resp_Party(Sub_Request_V,Main_Tree,Book,Report_Text,ME_clicked):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()

    #submit ME
    def Submit_ME():
        Resp_ME = Resp_MFG.get()
        ME_EXE_STRING = "EXEC Interactive.dbo.TM_Set_Resp_Party @id=?, @USER=?"
        c.execute(ME_EXE_STRING,ID,Resp_ME)

        e1 = "Responsible Party for Request " + ID + " was changed to " + Resp_ME + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
        Task_Manager.TM_Update_Change_Log(e1,Report_Text,ID)

        c.commit()
        c.close()
        top.destroy()
        top.update()

        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "Resp party for Request " + ID + " set to " + Resp_ME + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")

    if ID == 'None':
    #if no sub request selected, return that to user
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        #get the current status
        Status_EXE = "EXEC Interactive.dbo.TM_Get_Status @id=?"
        c.execute(Status_EXE,ID)
        statusdata = c.fetchall()
        statusarray = np.array(statusdata)
        Status = statusarray[0,0]
        if Status == "Initiated":
            #if request is in initiated, do not allow changing responsible party
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "You may only assign Responsible Parties to requests past initiated" + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
        else:
            top = Toplevel()
            top.geometry("500x500")
            top.title('My Second Window')

            #tell the user which ID they are changing the resp party of
            ID_Label = Label(top, text="Request #" + ID)
            ID_Label.grid(row=0, column=1, padx=5, pady=5)

            #connect to the Interactive to pull the list of users in ME and create a dropdown list
            ME_USERS_EXE_STRING = "EXEC Interactive.dbo.Populate_ME"
            c.execute(ME_USERS_EXE_STRING)
            ME_data = c.fetchall()
            ME_USERS = np.array(ME_data)
            ME_names = ["ME"]
            ME_rowcount = 0

            for row in ME_USERS:
                ME_names.append(ME_USERS[ME_rowcount,0].strip() + " " + ME_USERS[ME_rowcount,1].strip())
                ME_rowcount += 1
            Resp_MFG = StringVar()
            Resp_MFG.set(ME_names[0])

            ME_Users_Drop = OptionMenu(top,Resp_MFG, *ME_names)
            ME_Users_Drop.grid(row=1, column=1, padx=5, pady=5)

            Submit_ME_Button = Button(top, text="Set Responsible User", command=Submit_ME)
            Submit_ME_Button.grid(row=2, column=1, padx=5, pady=5)

            Task_Manager.TM_View_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)

    return
