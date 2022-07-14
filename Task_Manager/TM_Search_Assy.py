import pyodbc
import numpy as np
from tkinter import simpledialog
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees

#search for a specific assembly# and populate main tree accordingly
def TM_Search_Assy(Main_Tree,Book,Sub_Request_V,Report_Text):
    
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")

    c = conn2.cursor()
    
    Main_Trees.Clear_Main_Tree(Main_Tree)
    Main_Trees.Main_Tree_8(Main_Tree)

    ID = Sub_Request_V.get()

    if ID == None:
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "No Request Selected" + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")

    else:
        #Trap error if raised
        try:  

            Book.update()
            PCBA = simpledialog.askstring("PCBA#", "Enter the PCBA#")

            exe_String = "EXEC Interactive.dbo.TM_Search_Assy @pcba=?"
            data = c.execute(exe_String,PCBA)
            data = c.fetchall()
            np_data = np.array(data)
            
            Unique_Key_List = [] #Creating a Unique List of component requests to identify blocks of specific component requests
            Unique_Key_Row_List = []

            row_count = 0
            Unique_List = []
            for row in np_data: 
                
                if 1 == 1:
                    
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
            e1 = str(e)
            Report_Text.configure(state = NORMAL)
            Report_Text.delete('1.0',END)
            Report_Text.insert(END, e1 + "\n")
            Report_Text.configure(state = DISABLED)
            Report_Text.see("end")
                 
        c.commit()

        c.close()

    return