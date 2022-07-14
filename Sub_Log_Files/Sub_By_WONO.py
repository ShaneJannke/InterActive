import pyodbc
import numpy as np
from datetime import date
import os
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import Toplevel
from tkinter import Label
from tkinter import Entry
from tkinter import Button
import Main_Trees
import Sub_Log_Files


def Sub_By_WONO(Report_Text,Sub_Request_V,Main_Tree,Book):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=Interactive;"
                               "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()

    if ID == 'None':
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Sub Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
    else:
        #Status_EXE = "EXEC Interactive.dbo.SUB_Get_Status @id=?"
        #c.execute(Status_EXE,ID)
        #statusdata = c.fetchall()
        #statusarray = np.array(statusdata)
        #status = statusarray[0,0]
        #if status is not Initiated tell user
        #if status != "Initiated":
        #    Report_Text.configure(state = NORMAL)
        #    Report_Text.insert(END, "This button can only be used for Initiated Sub Requests" + "\n")
        #    Report_Text.configure(state = DISABLED)
        #    Report_Text.see("end")
        #if status is initiated, proceed with adding by WONO
        #else:
        top = Toplevel()
        top.geometry("300x250")
        top.title('Add By WO#')

        name = Label(top,text = "Sub Request #"+ID).pack()

        WOe1 = Label(top, text = "Work Order #").pack()
        e1 = Entry(top)
        e1.pack()

        PNe2 = Label(top, text = "Part Number").pack()
        e2 = Entry(top)
        e2.pack()

        Qtye3 = Label(top, text = "Quantity Needed").pack()
        e3 = Entry(top)
        e3.pack()

        btn = Button(top, text = "Submit", command = lambda: sub_submit(e1,e2,e3))
        btn.pack()

        def sub_submit(e1,e2,e3):

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

            WO = e1.get()
            PN = e2.get()
            Qty = e3.get() 
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
            #SO_exe_String = "EXEC Interactive.dbo.SUB_Get_SONO @id=?"
            #c.execute(SO_exe_String,ID)
            #data = c.fetchall()
            #SONOs = np.array(data)
            #SONO = SONOs[0,0]
            #if Sub Request has no SONO entered arleady, get sono from manex
            #if SONO == None:
            try:
                exe_String1 = "EXEC Interactive.dbo.SUB_Add_By_WONO @id=?, @iwo=?, @iPN=?, @iqty=?, @SC=?, @ME=?, @CAS=?"
                c.execute(exe_String1,ID,WO,PN,Qty,SC,ME,CAS) 
                Remove_Iniated_2 = "EXEC Interactive.dbo.SUB_Remove_Initated_ID_2" #This removed all iniated from the log that already have open/closed requests
                c.execute(Remove_Iniated_2)
                '''
                6/8/22 SJ
                Update the Current QTY table with the variable pulled earlier
                '''
                SET_QTY_STRING = "EXEC Interactive.dbo.SUB_Set_Curr_QTY @CurrQTY=?, @ID=?"
                c.execute(SET_QTY_STRING,CurrQTY,ID)

                e1 = "Work Order " + WO + " and Part Number " + PN + " added to Sub Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID) 

            except Exception as e:
                e1 = str(e)
                Report_Text.configure(state = NORMAL)
                Report_Text.delete('1.0',END)
                Report_Text.insert(END, e1 + "\n")
                Report_Text.configure(state = DISABLED)
                Report_Text.see("end")
            #if sub request has a SONO already entered, check that it is the same as the one found in manex
            #else:
            #    try:
            #        exe_String2 = "EXEC Interactive.dbo.SUB_Add_By_WONO_And_SONO @id=?, @iwo=?, @iPN=?, @iqty=?, @iso=?, @SC=?, @ME=?, @CAS=?"
             #       c.execute(exe_String2,ID,WO,PN,Qty,SONO,SC,ME,CAS) 
              #      Remove_Iniated_2 = "EXEC Interactive.dbo.SUB_Remove_Initated_ID_2" #This removed all iniated from the log that already have open/closed requests
               #     c.execute(Remove_Iniated_2) 
                '''
                6/8/22 SJ
                Update the Current QTY table with the variable pulled earlier
                '''
                #    SET_QTY_STRING = "EXEC Interactive.dbo.SUB_Set_Curr_QTY @CurrQTY=?, @ID=?"
                 #   c.execute(SET_QTY_STRING,CurrQTY,ID)

                  #  e1 = "Work Order " + WO + " and Part Number " + PN + " added to Sub Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
                   # Sub_Log_Files.Update_Sub_Change_Log(e1,Report_Text,ID)

                #except Exception as e:
                 #   e1 = str(e)
                  #  Report_Text.configure(state = NORMAL)
                  #  Report_Text.insert(END, e1 + "\n")
                   # Report_Text.configure(state = DISABLED)
                    #Report_Text.see("end")  

            c.commit()
            c.close()
            top.destroy()
            top.update()

            Main_Trees.Clear_Main_Tree(Main_Tree)
            Sub_Log_Files.View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)

        return

    return