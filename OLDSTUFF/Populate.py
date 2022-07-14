#Populates the Main View Tree with the table Interactive.dbo.sublog

from Clear import *
import pyodbc


def Sub_Log_Populate(Main_Tree):
    
    Clear_Main_Tree(Main_Tree)

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                    "Server=DC01;"
                    "Database=Interactive;"
                    "Trusted_Connection=yes;")

    c = conn2.cursor()
    
    #Trap error if raised
    try:  
        exe_String = "SELECT * FROM Interactive.dbo.sublog ORDER BY WONO"
        data = c.execute(exe_String) #Ordering by WONO because to avoid errors from the same Work Order being added at different times.
        data = c.fetchall()
      
        np_data = np.array(data)
        
        
        
        row_count = 0
        Unique_List = []
        
        for row in np_data: 
            


            if np_data[row_count,8] not in Unique_List:
                

                
                Unique_List.append(np_data[row_count,8])
                
                PrimaryID = len(Unique_List)
                
                if PrimaryID % 2 == 0:
                
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[1],row[2],row[3],row[5],row[4],row[6],row[7],row[8],row[9],row[10],row[11],row[19],row[12],row[13],row[14],row[15],row[16],row[17],row[18]),tags = "PrimaryRow")
                else:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[1],row[2],row[3],row[5],row[4],row[6],row[7],row[8],row[9],row[10],row[11],row[19],row[12],row[13],row[14],row[15],row[16],row[17],row[18]),tags = "SecondaryRow")
                
                Secondary_Row = 1
                
            else:  
                

                
                SecondaryID = str(PrimaryID) + "_" + str(Secondary_Row) #Secondary not not neaded, just kept in case we need to add extra informaiton to the log
                
                if PrimaryID % 2 == 0:
                
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[1],row[2],row[3],row[5],row[4],row[6],row[7],row[8],row[9],row[10],row[11],row[19],row[12],row[13],row[14],row[15],row[16],row[17],row[18]),tags = "PrimaryRow")
                    
                else:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[1],row[2],row[3],row[5],row[4],row[6],row[7],row[8],row[9],row[10],row[11],row[19],row[12],row[13],row[14],row[15],row[16],row[17],row[18]),tags = "SecondaryRow")
                    
                Secondary_Row = Secondary_Row + 1
            
            row_count = row_count + 1
        
    except Exception as e:
        #messagebox.showinfo("Results",e)
        self.e1 = str(e)
        self.Report_Text.configure(state = NORMAL)
        self.Report_Text.insert(END, self.e1 + "\n")
        self.Report_Text.configure(state = DISABLED)
        self.Report_Text.see("end")
             
    c.commit()

    c.close()
    
    
    return