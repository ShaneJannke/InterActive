import pyodbc
import numpy as np
from tkinter import simpledialog
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
from tkinter import messagebox
import Main_Trees

def Sub_Alt_History(Main_Tree,Report_Text,Book):

    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                       "Server=DC01;"
                       "Database=Interactive;"
                       "Trusted_Connection=yes;")
    c = conn2.cursor()


    Book.update()
    PN = simpledialog.askstring("PN", "Enter the Part Number")

    if PN == None:
        pass
        
    else:
            
        EXE_STRING ="EXEC Interactive.dbo.SUB_Alt_History @ipn=?"
                

        try:
            c.execute(EXE_STRING,PN)
            data = c.fetchall()
            if not data:
                messagebox.showerror("PN Alt History", "No data found.")
            else:
                '''
                Uses Main_Tree_9 to show different data
                '''
                Main_Trees.Clear_Main_Tree(Main_Tree)
                Main_Trees.Main_Tree_9(Main_Tree)
                np_data = np.array(data)
                
                row_count = 0
                Unique_List = []
                
                for row in np_data: 
                    if np_data[row_count,0] not in Unique_List:
                        Unique_List.append(np_data[row_count,0])
                        
                        PrimaryID = len(Unique_List)
                        
                        if PrimaryID % 2 == 0:
                            Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags = "PrimaryRow")
                        else:
                            Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags = "SecondaryRow")
                        
                        Secondary_Row = 1
                        
                    else:  
                        SecondaryID = str(PrimaryID) + "_" + str(Secondary_Row) #Secondary not not neaded, just kept in case we need to add extra informaiton to the log
                        
                        if PrimaryID % 2 == 0:
                            Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags = "PrimaryRow")
                            
                        else:
                            Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags = "SecondaryRow")
                            
                        Secondary_Row = Secondary_Row + 1
                    
                    row_count = row_count + 1

                Report_Text.configure(state = NORMAL)
                Report_Text.delete('1.0',END)
                Report_Text.insert(END, "Viewing Alternates for PN: " + PN + "\n")
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

    return 