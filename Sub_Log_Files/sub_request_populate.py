import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees

def sub_request_populate(Main_Tree,Sub_Options_V,Report_Text,Sub_clicked):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                       "Server=DC01;"
                       "Database=Interactive;"
                       "Trusted_Connection=yes;")
    c = conn2.cursor()
    '''
    Uses Main_Tree_6 as it does not have PO Placed By column
    '''
    Main_Trees.Clear_Main_Tree(Main_Tree)
    Main_Trees.Main_Tree_6(Main_Tree)

    '''
    6/7/22 SJ
    Get the selected Responsible Party to search alongside the selected status
    '''
    User = Sub_clicked.get()
        
    EXE_STRING ="EXEC Interactive.dbo.SUB_By_Status @status=?, @User=?"
    
    #Trap error if raised
    try:
        result = Sub_Options_V.get().replace("Select ", "")
            
        c.execute(EXE_STRING,result,User)
        data = c.fetchall()
        np_data = np.array(data)
        
        row_count = 0
        Unique_List = []
        
        for row in np_data: 
            if np_data[row_count,0] not in Unique_List:
                Unique_List.append(np_data[row_count,0])
                
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