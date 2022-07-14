import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees

#code mostly copied from Sub Log
def TM_populate_status(Main_Tree,TM_Options_V,Report_Text,ME_clicked):

    Main_Trees.Clear_Main_Tree(Main_Tree)
    Main_Trees.Main_Tree_8(Main_Tree)

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                       "Server=DC01;"
                       "Database=Interactive;"
                       "Trusted_Connection=yes;")
    c = conn2.cursor()
    
    EXE_STRING ="EXEC Interactive.dbo.TM_Populate_Status @status=?, @USER=?"

    result = TM_Options_V.get()

    if result == "Select Initiated":
        option_1 = "Initiated"
    elif result == "Select Open":
        option_1 = "Open"
    elif result == "Select In Progress":
        option_1 = "In Progress"
    elif result == "Select Pending Review":
        option_1 = "Pending Review"
    elif result == "Select Rejected":
        option_1 = "Rejected"
    elif result == "Select Closed":
        option_1 = "Closed"

    User = ME_clicked.get()

    #Trap error if raised
    try:
        c.execute(EXE_STRING, option_1,User)
        data = c.fetchall()
        np_data = np.array(data)
        
        row_count = 0
        Unique_List = []
        
        for row in np_data: 
            if np_data[row_count,0] not in Unique_List:
                Unique_List.append(np_data[row_count,0])
                
                PrimaryID = len(Unique_List)
                
                if PrimaryID % 2 == 0:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[10],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]),tags = "PrimaryRow")
                else:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[10],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]),tags = "SecondaryRow")
                
                Secondary_Row = 1
                
            else: 
                SecondaryID = str(PrimaryID) + "_" + str(Secondary_Row) #Secondary not not neaded, just kept in case we need to add extra informaiton to the log
                
                if PrimaryID % 2 == 0:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[10],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]),tags = "PrimaryRow")
                    
                else:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[10],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]),tags = "SecondaryRow")
                    
                Secondary_Row = Secondary_Row + 1
            
            row_count = row_count + 1
        
    except Exception as e:
        #messagebox.showinfo("Results",e)
        e1 = str(e)
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, e1 + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
             
    c.commit()
    c.close()

    return 