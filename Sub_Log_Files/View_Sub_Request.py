import pyodbc
import numpy as np
from tkinter import simpledialog
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees

def View_Sub_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text):
    
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")

    c = conn2.cursor()
    
    Main_Trees.Clear_Main_Tree(Main_Tree)
    Main_Trees.Main_Tree_6(Main_Tree)

    if ID == None:
        Book.update()
        ID = simpledialog.askstring("ID#", "Enter the Sub Request ID#")
    
    #Trap error if raised
    try:  
        exe_String = "EXEC Interactive.dbo.SUB_By_ID @id=?"
        data = c.execute(exe_String,ID)
        data = c.fetchall()
        np_data = np.array(data)

        Sub_Request_V.set(ID)
        
        Unique_Key_List = [] #Creating a Unique List of component requests to identify blocks of specific component requests
        Unique_Key_Row_List = []

        row_count = 0
        Unique_List = []
        for row in np_data: 
            
            if str(np_data[row_count,5])+str(np_data[row_count,13])+str(np_data[row_count,11]) not in Unique_Key_List:
                Unique_Key_List.append(str(np_data[row_count,5])+str(np_data[row_count,13])+str(np_data[row_count,11]))
                
                Unique_List.append(np_data[row_count,8])
                
                PrimaryID = len(Unique_List)
                
                if PrimaryID % 2 == 0:
                
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[3],row[4],row[5],row[8],row[7],row[6],row[9],row[18],row[11],row[10],row[13],row[14],row[12],row[20],row[21],row[22],row[15],row[16],row[17],row[19],row[2],row[1]),tags = "PrimaryRow")
                else:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[3],row[4],row[5],row[8],row[7],row[6],row[9],row[18],row[11],row[10],row[13],row[14],row[12],row[20],row[21],row[22],row[15],row[16],row[17],row[19],row[2],row[1]),tags = "SecondaryRow")
                
                Secondary_Row = 1
                
            else:  
                
                SecondaryID = str(PrimaryID) + "_" + str(Secondary_Row) #Secondary not not neaded, just kept in case we need to add extra informaiton to the log
                
                if PrimaryID % 2 == 0:
                
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[3],row[4],row[5],row[8],row[7],row[6],row[9],row[18],row[11],row[10],row[13],row[14],row[12],row[20],row[21],row[22],row[15],row[16],row[17],row[19],row[2],row[1]),tags = "PrimaryRow")
                    
                else:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[3],row[4],row[5],row[8],row[7],row[6],row[9],row[18],row[11],row[10],row[13],row[14],row[12],row[20],row[21],row[22],row[15],row[16],row[17],row[19],row[2],row[1]),tags = "SecondaryRow")
                    
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