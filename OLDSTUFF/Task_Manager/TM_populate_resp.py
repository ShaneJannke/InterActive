import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees

def TM_populate_resp(Main_Tree,ME_clicked,Report_Text):

    Main_Trees.Clear_Main_Tree(Main_Tree)
    Main_Trees.Main_Tree_7(Main_Tree)

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                       "Server=DC01;"
                       "Database=Testdatabase;"
                       "Trusted_Connection=yes;")
    c = conn2.cursor()
    
    EXE_STRING ="EXEC Testdatabase.dbo.TM_Populate_Resp @USER=?"
    User = ME_clicked.get()
    #Trap error if raised
    try:
        c.execute(EXE_STRING, User)
        data = c.fetchall()
        np_data = np.array(data)
        
        row_count = 0
        Unique_List = []
        
        for row in np_data: 
            if np_data[row_count,0] not in Unique_List:
                Unique_List.append(np_data[row_count,0])
                
                PrimaryID = len(Unique_List)
                
                if PrimaryID % 2 == 0:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0].strip(),row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]),tags = "PrimaryRow")
                else:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0].strip(),row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]),tags = "SecondaryRow")
                
                Secondary_Row = 1
                
            else: 
                SecondaryID = str(PrimaryID) + "_" + str(Secondary_Row) #Secondary not not neaded, just kept in case we need to add extra informaiton to the log
                
                if PrimaryID % 2 == 0:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0].strip(),row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]),tags = "PrimaryRow")
                    
                else:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0].strip(),row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]),tags = "SecondaryRow")
                    
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