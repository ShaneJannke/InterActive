import pyodbc
import numpy as np
from tkinter import Tk
from tkinter import Entry
from tkinter import Label
from tkinter import Button
from tkinter import ttk
import Main_Trees

def TM_Search_Assy(Main_Tree, root):

    app_width = 400
    app_height = 200

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    app_width_loc = int(screen_width/2 - app_width/2)
    app_height_loc = int(screen_height/2 - app_height/2)

    Assy_Search = Tk()    
    Assy_Search.title('Search by Assy')
    Assy_Search.iconbitmap('S:\\_ENG_MANUFACTURING\\Applications\\Inter-Active\\Launcher\\Icon.ico')
    Assy_Search.geometry(f'{app_width}x{app_height}+{app_width_loc}+{app_height_loc}')

    #Search Button
    def search_now():
        Main_Trees.Clear_Main_Tree(Main_Tree)
        conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                                "Server=DC01;"
                                "Database=Testdatabase;"
                                "Trusted_Connection=yes;")     
        c = conn2.cursor()   
        searched = search_box.get()
        searched2 = search_box2.get()
        if len(searched) == 0:
            #if both searches empty, return everything
            if len(searched2) == 0:
                EXE_STRING ="EXEC Testdatabase.dbo.TM_Populate"   
                c.execute(EXE_STRING)
            #if only rev entered, search by rev
            else:
                EXE_STRING ="EXEC Testdatabase.dbo.TM_Search_By_Rev @Rev=?"
                c.execute(EXE_STRING, searched2)
        else:
            #if only assembly entered, search by assy
            if len(searched2) == 0:
                EXE_STRING ="EXEC Testdatabase.dbo.TM_Search_By_Assy @Assy=?"
                c.execute(EXE_STRING, searched)
            #if both searches filled, search by assembly and rev    
            else:
                EXE_STRING = "EXEC Testdatabase.dbo.TM_Search_By_Assy_And_Rev @Assy=?, @Rev=?"
                c.execute(EXE_STRING, searched, searched2)
            
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
                
        Assy_Search.destroy()
        c.commit()
        c.close() 

    #assembly search box
    search_box = Entry(Assy_Search, font=("Helvetica", 10))
    search_box.grid(row=0, column=1, padx=10, pady=10)
    #Rev Search Box
    search_box2 = Entry(Assy_Search, font=("Helvetica", 10))
    search_box2.grid(row=1, column=1, padx=10, pady=10)

    #assembly search label
    search_box_label = Label(Assy_Search, text="Search an Assembly", font=("Helvetica", 10))
    search_box_label.grid(row=0, column=0, padx=10, pady=10)
    #Rev search label
    search_box_label2 = Label(Assy_Search, text="Assembly REV", font=("Helvetica", 10))
    search_box_label2.grid(row=1, column=0, padx=10, pady=10)

    #Entry box search button
    search_button = Button(Assy_Search, text="Search Assembly", command=search_now)
    search_button.grid(row=2, column=0, padx=10)
        
    return