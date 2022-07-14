import numpy as np
import pyodbc
from functools import partial
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Sub_Log_Files
import Task_Manager

def MoreInfo(Report_Text, Sub_Request_V, e):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Testdatabase;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()

    PCBA = Sub_Request_V.get()

    if PCBA == 'None':

        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No PCBA Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")

    else:
        EXE_STRING = "EXEC Testdatabase.dbo.TM_More_Info @PCBA=?"
        c.execute(EXE_STRING,PCBA)
        data = c.fetchall()
        np_data = np.array(data)

        WO = str(np_data[0,0])
        WO = WO.replace(r'\n','\n')
        WO = WO.replace(r'\t','\t')
        WO = WO.replace(r'\r','\r')



        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "PCBA " + PCBA + " Info\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")

        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, "WO #" + WO + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")

        if len(np_data) == 1:
            stencil = str(np_data[0,1])
            stencil = stencil.replace(r'\n','\n')
            stencil = stencil.replace(r'\t','\t')
            stencil = stencil.replace(r'\r','\r')

            Report_Text.configure(state = NORMAL)
            Report_Text.insert(END, "Stencils: " + stencil + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("1.0")
        else:

            stencil1 = str(np_data[0,1].strip())
            stencil1 = stencil1.replace(r'\n','\n')
            stencil1 = stencil1.replace(r'\t','\t')
            stencil1 = stencil1.replace(r'\r','\r')

            stencil2 = str(np_data[1,1].strip())
            stencil2 = stencil2.replace(r'\n','\n')
            stencil2 = stencil2.replace(r'\t','\t')
            stencil2 = stencil2.replace(r'\r','\r')

            x = 2
            if stencil1 == stencil2:
                for x in range(2,len(np_data)):
                    stencil2 = str(np_data[x,1].strip())
                    stencil2 = stencil2.replace(r'\n','\n')
                    stencil2 = stencil2.replace(r'\t','\t')
                    stencil2 = stencil2.replace(r'\r','\r')
                    x += 1
                    if stencil1 == stencil2 and x == len(np_data):
                        Report_Text.configure(state = NORMAL)
                        Report_Text.insert(END, "Stencils: " + stencil1 + "\n")
                        Report_Text.configure(state = DISABLED)
                        Report_Text.see("1.0")
                        break
                    elif stencil1 != stencil2 and x == len(np_data):
                        Report_Text.configure(state = NORMAL)
                        Report_Text.insert(END, "Stencils: " + stencil1 + " " + stencil2 + "\n")
                        Report_Text.configure(state = DISABLED)
                        Report_Text.see("1.0")
                        break
                    elif x != len(np_data):
                        pass
            else:
                Report_Text.configure(state = NORMAL)
                Report_Text.insert(END, "Stencils: " + stencil1 + " " + stencil2 + "\n")
                Report_Text.configure(state = DISABLED)
                Report_Text.see("1.0")


        feedback = str(np_data[0,2])
        feedback = feedback.replace(r'\n','\n')
        feedback = feedback.replace(r'\t','\t')
        feedback = feedback.replace(r'\r','\r')

        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, "Prod Feedback: " + feedback + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")  

        CustName = str(np_data[0,3])
        CustName = CustName.replace(r'\n','\n')
        CustName = CustName.replace(r'\t','\t')
        CustName = CustName.replace(r'\r','\r')

        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, "Customer: " + CustName + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")

        CustPN = str(np_data[0,4])
        CustPN = CustPN.replace(r'\n','\n')
        CustPN = CustPN.replace(r'\t','\t')
        CustPN = CustPN.replace(r'\r','\r')

        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, "Customer PN: " + CustPN + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")

        CustRev = str(np_data[0,5])
        CustRev = CustRev.replace(r'\n','\n')
        CustRev = CustRev.replace(r'\t','\t')
        CustRev = CustRev.replace(r'\r','\r')

        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, "Customer Rev: " + CustRev + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")

        PCBA_Desc = str(np_data[0,6])
        PCBA_Desc = PCBA_Desc.replace(r'\n','\n')
        PCBA_Desc = PCBA_Desc.replace(r'\t','\t')
        PCBA_Desc = PCBA_Desc.replace(r'\r','\r')

        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, "PCBA Desc: " + PCBA_Desc + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")

        Inv_Note = str(np_data[0,7])
        Inv_Note = Inv_Note.replace(r'\n','\n')
        Inv_Note = Inv_Note.replace(r'\t','\t')
        Inv_Note = Inv_Note.replace(r'\r','\r')

        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, "Inv Note: " + Inv_Note + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")

    return