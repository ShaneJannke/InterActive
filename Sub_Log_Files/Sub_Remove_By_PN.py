import pyodbc
import os
import numpy as np
from datetime import date
from tkinter import simpledialog
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import Toplevel
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox
import Main_Trees
import Sub_Log_Files

def Sub_Remove_By_PN(Sub_Request_V,Book,Report_Text,Main_Tree,Sub_Options_V,Sub_clicked):
    
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
        top = Toplevel()
        top.geometry("200x200")
        top.title('My Second Window')

        name = Label(top,text = "Sub Request #"+ID).pack()

        WOe1 = Label(top, text = "Work Order #").pack()
        e1 = Entry(top)
        e1.pack()

        PNe2 = Label(top, text = "Part Number").pack()
        e2 = Entry(top)
        e2.pack()
        
        btn = Button(top, text = "Submit", command = lambda: sub_submit(e1,e2))
        btn.pack()

        def sub_submit(e1,e2):
            EXE_STRING ="EXEC Interactive.dbo.SUB_Remove_By_PN @ID=?, @iPN=?, @iwo=?"
            EXE_COUNT_STRING ="EXEC Interactive.dbo.SUB_PN_Count @ID=?, @iwo=?"

            WO = e1.get()
            PN = e2.get()

            try:
                #check if this is the last PN attached to the sub request
                c.execute(EXE_COUNT_STRING,ID,WO)
                countdata = c.fetchall()
                countarray = np.array(countdata)
                pncount = countarray[0,0]
                wocount = countarray[0,1]
                #if this is the last PN, confirm that the user wants to delete it
                if pncount == 1 and wocount == 1:
                    Delete_Confirm = messagebox.askquestion("Delete?", "This is the last PN attached and will delete the request, continue?", icon='warning')
                    if Delete_Confirm == 'yes':

                        #Trap error if raised
                        try:
                            c.execute(EXE_STRING,ID,PN,WO)

                            e1 = "Part Number " + PN + " was removed from Sub Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
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

                        Main_Trees.Clear_Main_Tree(Main_Tree)
                        Sub_Log_Files.sub_request_populate(Main_Tree,Sub_Options_V,Report_Text,Sub_clicked)
                        Sub_Request_V.set(None) 

                    else:
                        top.destroy()
                        top.update()
                #if count greater than 1, execute without asking
                else:  

                    #Trap error if raised
                    try:
                        c.execute(EXE_STRING,ID,PN,WO)

                        e1 = "Part Number " + PN + " was removed from Sub Request " + ID + " by " + os.getlogin() + " on " + str(date.today().strftime("%m/%d/%Y"))
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

                    Main_Trees.Clear_Main_Tree(Main_Tree)
                    Sub_Log_Files.View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text) 

            except Exception as e:
                e1 = str(e)
                Report_Text.configure(state = NORMAL)
                Report_Text.delete('1.0',END)
                Report_Text.insert(END, e1 + "\n")
                Report_Text.configure(state = DISABLED)
                Report_Text.see("end")
        

    
    return