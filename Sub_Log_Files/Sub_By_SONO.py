from datetime import date
import os
import numpy as np
import pyodbc
from tkinter import Toplevel
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees
import Sub_Log_Files

#removed Sub_Options_V as it was not used
def Sub_By_SONO(Sub_Request_V,Main_Tree,Book,Report_Text):

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
        Status_EXE = "EXEC Interactive.dbo.SUB_Get_Status @id=?"
        c.execute(Status_EXE,ID)
        statusdata = c.fetchall()
        statusarray = np.array(statusdata)
        status = statusarray[0,0]

        #if status is not initiated, tell user and do not proceed
        if status != "Initiated":
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, "This button can only be used for Initiated Sub Requests" + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
        else:
            top = Toplevel()
            top.geometry("300x300")
            top.title('Add By SO#')

            name = Label(top,text = "Sub Request #"+ID).pack()

            WOe1 = Label(top, text = "Sales Order #").pack()
            e1 = Entry(top)
            e1.pack()

            PNe2 = Label(top, text = "Part Number").pack()
            e2 = Entry(top)
            e2.pack()

            PCBAe3 = Label(top, text = "PCBA #").pack()
            e3 = Entry(top)
            e3.pack()

            Qtye4 = Label(top, text = "Quantity Needed").pack()
            e4 = Entry(top)
            e4.pack()

            btn = Button(top, text = "Submit", command = lambda: sub_submit(e1.get(),e2.get(),e3.get(),e4.get()))
            btn.pack(pady=10)


        def sub_submit(e1,e2,e3,e4):

            #get stored responsible SC from database per selected Sub Request ID
            SC_EXE_STRING = "EXEC Interactive.dbo.SUB_Get_Resp_SC @ID=?"
            c.execute(SC_EXE_STRING,ID)
            #format the data to remove brackets and quotes
            SC_data = c.fetchall()
            respSC = np.array(SC_data)
            SC = respSC[0,0]

            #get stored responsible ME from database per selected Sub Request ID
            ME_EXE_STRING = "EXEC Interactive.dbo.SUB_Get_Resp_ME @ID=?"
            c.execute(ME_EXE_STRING,ID)
            #format the data to remove brackets and quotes
            ME_data = c.fetchall()
            respME = np.array(ME_data)
            ME = respME[0,0]

            #get stored responsible CAS from database per selected Sub Request ID
            CAS_EXE_STRING = "EXEC Interactive.dbo.SUB_Get_Resp_CAS @ID=?"
            c.execute(CAS_EXE_STRING,ID)
            #format the data to remove brackets and quotes
            CAS_data = c.fetchall()
            respCAS = np.array(CAS_data)
            CAS = respCAS[0,0]

            SO = e1
            PN = e2
            PCBA = e3
            Qty = e4

            '''
            6/8/22 SJ
            get the current QTY of PN from manex
            '''
            GET_QTY_STRING = "EXEC Interactive.dbo.SUB_Get_Curr_QTY @pn=?"
            c.execute(GET_QTY_STRING,PN)
            QTYdata = c.fetchall()
            QTYarray = np.array(QTYdata)
            CurrQTY = QTYarray[0,0]
            
            #get SONO from database for given ID
            SO_exe_String = "EXEC Interactive.dbo.SUB_Get_SONO @id=?"
            c.execute(SO_exe_String,ID)
            data = c.fetchall()
            SONOs = np.array(data)
            SONO = SONOs[0,0]
            #if SONO from database is the same as SO entered by user, or if sub request has no SONO attached >> insert data
            if SO == SONO or SONO == None:         
                try:
                    exe_String = "EXEC Interactive.dbo.SUB_Add_By_SONO @id=?, @iso=?, @ipn=?, @ipcba=?, @iqty=?, @SC=?, @ME=?, @CAS=?"
                    c.execute(exe_String,ID,SO,PN,PCBA,Qty,SC,ME,CAS) 
                    Remove_Iniated_2 = "EXEC Interactive.dbo.SUB_Remove_Initated_ID_2" #This removed all iniated from the log that already have open/closed requests
                    c.execute(Remove_Iniated_2)
                    '''
                    6/8/22 SJ
                    Update the Current QTY table with the variable pulled earlier
                    '''
                    SET_QTY_STRING = "EXEC Interactive.dbo.SUB_Set_Curr_QTY @CurrQTY=?, @ID=?"
                    c.execute(SET_QTY_STRING,CurrQTY,ID)
                    
                    e1 = "Sales Order " + SO + " and Part Number " + PN + " added to Sub Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                    Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID)

                except Exception as e:
                    e1 = str(e)
                    Report_Text.configure(state = NORMAL)
                    Report_Text.delete('1.0',END)
                    Report_Text.insert(END, e1 + "\n")
                    Report_Text.configure(state = DISABLED)
                    Report_Text.see("end")
            #if SONO from database is different than the entered SO >> do not enter and notify user
            else:
                Report_Text.configure(state = NORMAL)
                Report_Text.delete('1.0',END)
                Report_Text.insert(END, "Sub Request already has a different SONO attached, please make a new request" + "\n")
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