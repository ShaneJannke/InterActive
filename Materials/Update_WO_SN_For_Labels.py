from tkinter import simpledialog
from tkinter import NORMAL
from tkinter import DISABLED
from tkinter import END
import pyodbc
import os


#Create a button function "Print Labels" frame4
def Update_WO_SN_For_Labels(Book,Report_Text):
    Book.update()       
    WO = simpledialog.askstring("WONO", "Enter the Work Order Number")
    Book.update()
    Label_Type = simpledialog.askstring("35-XXXX", "Enter the Label Part Number")

    if WO == None:
        return

    elif Label_Type == "35-0019": #5/16/2022 NS - Adding a catch so we dont try to print Ultratec labels with the original function.
        input1 = "EXEC ManexExtras.utec.W_Update_SN_Labels @iwo=?"

    elif Label_Type == "35-0020":
        input1 = "EXEC ManexExtras.utec.W_Update_SN_Labels @iwo=?"

    elif Label_Type == "35-0021":
        input1 = "EXEC ManexExtras.utec.W_Update_SN_Labels @iwo=?"

    elif Label_Type == None:
        return

    else:
        input1 = "EXEC ManexExtras.dbo.P_Update_WO_SN_For_Labels @woi=?"

    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                    "Server=DC01;"
                    "Database=ManexExtras;"
                    "Trusted_Connection=yes;")

    #Create Cursor    
    c = conn.cursor()
    
    #Trap error if raised
    try:
        c.execute(input1, WO)
    except Exception as e:
        e1 = str(e)
        
        Report_Text.configure(state = NORMAL)
        Report_Text.insert(END, e1 + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")

    c.commit()

    c.close()  

    print(input1)
    
    os.startfile("H:\\_LABELS\\Standard Labels\\" + Label_Type + ".BWS")
    return