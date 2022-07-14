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
import Sub_Log_Files

#get the selected name from CAS dropdown and insert it as the responsible party for selected Sub Request
#removed book, frame5 as it was not used
def Sub_Set_Resp_Party(Sub_clicked,Sub_Request_V,Main_Tree,Report_Text,Sub_Options_V,Book):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()

    #submit Supply Chain
    def Submit_SC():
        Resp_SC = Resp_Supply.get()
        SC_EXE_STRING = "EXEC Interactive.dbo.SUB_Set_Resp_SC @ID=?, @USER=?"
        c.execute(SC_EXE_STRING,ID,Resp_SC)

        e1 = "Responsible Supply Chain for Sub Request " + ID + " was changed to " + Resp_SC + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
        Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID)

        c.commit()
        top.destroy()
        top.update()

    #submit ME
    def Submit_ME():
        Resp_ME = Resp_MFG.get()
        ME_EXE_STRING = "EXEC Interactive.dbo.SUB_Set_Resp_ME @ID=?, @USER=?"
        c.execute(ME_EXE_STRING,ID,Resp_ME)

        e1 = "Responsible ME for Sub Request " + ID + " was changed to " + Resp_ME + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
        Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID)
        c.commit()
        top.destroy()
        top.update()

    #submit CAS
    def Submit_CAS():
        Resp_CAS = Resp_CustServ.get()
        CAS_EXE_STRING = "EXEC Interactive.dbo.SUB_Set_Resp_CAS @ID=?, @USER=?"
        c.execute(CAS_EXE_STRING,ID,Resp_CAS)
        e1 = "Responsible CAS for Sub Request " + ID + " was changed to " + Resp_CAS + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
        Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID)

        c.commit()
        top.destroy()
        top.update()

    if ID == 'None':
    #if no sub request selected, return that to user
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Sub Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        #get the current status
        Status_EXE = "EXEC Interactive.dbo.SUB_Get_Status @id=?"
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
            ID_Label = Label(top, text="Sub Request #" + ID)
            ID_Label.grid(row=0, column=1, padx=5, pady=5)

            #connect to the Interactive to pull the list of users in Supply Chain, and create a dropdown list
            SC_USERS_EXE_STRING = "EXEC Interactive.dbo.SUB_Populate_SC"
            c.execute(SC_USERS_EXE_STRING)
            SC_data = c.fetchall()
            SC_USERS = np.array(SC_data)
            SC_names = ["Supply Chain"]
            SC_rowcount = 0

            for row in SC_USERS:
                SC_names.append(SC_USERS[SC_rowcount,0].strip() + " " + SC_USERS[SC_rowcount,1].strip())
                SC_rowcount += 1
            Resp_Supply = StringVar()
            Resp_Supply.set(SC_names[0])

            SC_Users_Drop = OptionMenu(top,Resp_Supply, *SC_names)
            SC_Users_Drop.grid(row=1, column=0, padx=5, pady=5)

            Submit_SC_Button = Button(top, text="Set Responsible Supply Chain", command=Submit_SC)
            Submit_SC_Button.grid(row=2, column=0, padx=5, pady=5)


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

            Submit_ME_Button = Button(top, text="Set Responsible ME", command=Submit_ME)
            Submit_ME_Button.grid(row=2, column=1, padx=5, pady=5)


            #connect to the Interactive to pull the list of users in CAS and create a dropdown list
            CAS_USERS_EXE_STRING = "EXEC Interactive.dbo.SUB_Populate_CAS"
            c.execute(CAS_USERS_EXE_STRING)
            CAS_data = c.fetchall()
            CAS_USERS = np.array(CAS_data)
            CAS_names = ["CAS"]
            CAS_rowcount = 0

            for row in CAS_USERS:
                CAS_names.append(CAS_USERS[CAS_rowcount,0].strip() + " " + CAS_USERS[CAS_rowcount,1].strip())
                CAS_rowcount += 1
            Resp_CustServ = StringVar()
            Resp_CustServ.set(CAS_names[0])

            CAS_Users_Drop = OptionMenu(top,Resp_CustServ, *CAS_names)
            CAS_Users_Drop.grid(row=1, column=2, padx=5, pady=5)

            Submit_CAS_Button = Button(top, text="Set Responsible CAS", command=Submit_CAS)
            Submit_CAS_Button.grid(row=2, column=2, padx=5, pady=5)

            Sub_Log_Files.View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)

    return
