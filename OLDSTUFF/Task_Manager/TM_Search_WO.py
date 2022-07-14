import pyodbc
import numpy as np
from tkinter import Tk
from tkinter import Entry
from tkinter import Label
from tkinter import Button
from tkinter import ttk
import Main_Trees

def TM_Search_WO(Main_Tree, root):

    app_width = 400
    app_height = 150

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    app_width_loc = int(screen_width/2 - app_width/2)
    app_height_loc = int(screen_height/2 - app_height/2)

    WO_Search = Tk()    
    WO_Search.title('Search by Work Order')
    WO_Search.iconbitmap('S:\\_ENG_MANUFACTURING\\Applications\\Inter-Active\\Launcher\\Icon.ico')
    WO_Search.geometry(f'{app_width}x{app_height}+{app_width_loc}+{app_height_loc}')

    def search_now():
        Main_Trees.Clear_Main_Tree(Main_Tree)
        conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                                "Server=DC01;"
                                "Database=Testdatabase;"
                                "Trusted_Connection=yes;")     
        c = conn2.cursor()   
        searched = search_box.get()
        #if search box is empty, return all results
        if len(searched) == 0:
            EXE_STRING ="EXEC Testdatabase.dbo.TM_Populate"   
            c.execute(EXE_STRING)
        #if search is filled, search by Work Order
        else:
            EXE_STRING ="EXEC Testdatabase.dbo.TM_Search_By_WONO @WorkOrder=?"
            c.execute(EXE_STRING, searched)

        data = c.fetchall()
        np_data = np.array(data)
        
        row_count = 0
        Unique_List = []
        
        for row in np_data: 
            if np_data[row_count,0] not in Unique_List:
                Unique_List.append(np_data[row_count,0])
                
                PrimaryID = len(Unique_List)
                
                if PrimaryID % 2 == 0:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags = "PrimaryRow")
                else:
                    Main_Tree.insert(parent ='', index= 'end', iid = PrimaryID, text="", values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags = "SecondaryRow")
                
                Secondary_Row = 1
                
            else:  
                SecondaryID = str(PrimaryID) + "_" + str(Secondary_Row) #Secondary not not neaded, just kept in case we need to add extra informaiton to the log
                
                if PrimaryID % 2 == 0:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags = "PrimaryRow")
                    
                else:
                    Main_Tree.insert(PrimaryID, index= 'end', iid= SecondaryID, text="", values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]),tags = "SecondaryRow")
                    
                Secondary_Row = Secondary_Row + 1
            
            row_count = row_count + 1
                
        WO_Search.destroy()
        c.commit()
        c.close() 

    def search_now_enter(e):
        search_now()

    #assembly search box
    search_box = Entry(WO_Search, font=("Helvetica", 10))
    search_box.grid(row=0, column=1, padx=10, pady=10)

    #assembly search label
    search_box_label = Label(WO_Search, text="Search for Work Order", font=("Helvetica", 10))
    search_box_label.grid(row=0, column=0, padx=10, pady=10)

    #Entry box search button
    search_button = Button(WO_Search, text="Search Work Order", command=search_now)
    search_button.grid(row=2, column=0, padx=10)

    WO_Search.bind('<Return>',search_now_enter)
        
    return