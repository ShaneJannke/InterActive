import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Sub_Log_Files
import Main_Trees
import TM_Remake

#New sub request button
def New_TM_Request(Main_Tree,Sub_Request_V,Report_Text,Book):
    
    Main_Trees.Clear_Main_Tree(Main_Tree)
    
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                       "Server=DC01;"
                       "Database=Testdatabase;"
                       "Trusted_Connection=yes;")
    c = conn2.cursor()
        
    Generate = "EXEC Testdatabase.dbo.TM_Generate_Request_ID"
    Remove_Iniated_1 = "EXEC Testdatabase.dbo.TM_Remove_Initated_ID_1" #This removes all intiated from the log
    Remove_Iniated_2 = "EXEC Testdatabase.dbo.TM_Remove_Initated_ID_2" #This removed all iniated from the log that already have open/closed requests
    
    #Trap error if raised
    try:  
        c.execute(Remove_Iniated_1)
        c.execute(Generate)
        '''
        could make this into a SQL procedure - works fine as is but would be more consistent
        '''
        get_data = "SELECT MAX(REQUEST_ID) FROM [Testdatabase].[dbo].[TM_REQUEST_ID_GENERATOR] "
        c.execute(get_data)
        data1 = c.fetchall()
        np_data = np.array(data1)
        ID = str(np_data[:,0])
        ID = ID[1:-1]
        c.execute(Remove_Iniated_2)
        
        exe_String = "EXEC Testdatabase.dbo.TM_By_ID @id=?"
        data2 = c.execute(exe_String,ID)
        data2 = c.fetchall()
        np_data = np.array(data2)

        Sub_Request_V.set(ID)
        
        row_count = 0
        Unique_List = []
        
        for row in np_data: 
            if np_data[row_count,8] not in Unique_List:
                Unique_List.append(np_data[row_count,8])
                
                PrimaryID = len(Unique_List)
                
                if PrimaryID % 2 == 0:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[10],row[1],row[5],row[8],row[7],row[6],row[9],row[4],row[2],row[3]),tags = "PrimaryRow")
                else:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[10],row[1],row[5],row[8],row[7],row[6],row[9],row[4],row[2],row[3]),tags = "SecondaryRow")
                
                Secondary_Row = 1
                
            else:  
                SecondaryID = str(PrimaryID) + "_" + str(Secondary_Row) #Secondary not not neaded, just kept in case we need to add extra informaiton to the log
                
                if PrimaryID % 2 == 0:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[10],row[1],row[5],row[8],row[7],row[6],row[9],row[4],row[2],row[3]),tags = "PrimaryRow")
                    
                else:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[10],row[1],row[5],row[8],row[7],row[6],row[9],row[4],row[2],row[3]),tags = "SecondaryRow")
                    
                Secondary_Row = Secondary_Row + 1
            
            row_count = row_count + 1
        
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, "TM Request "+ ID +" has been generated.\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")

    except Exception as e:
        e1 = str(e)
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, e1 + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("end")
             
    c.commit()
    c.close()

    TM_Remake.View_TM_Request(ID,Main_Tree,Book,Sub_Request_V,Report_Text)

    return