import os
from tkinter import simpledialog
import csv

def Export_Main_Tree(Main_Tree,Book):
    
    
    USERNAME = os.getlogin()
    
    param = []

    for line in Main_Tree.get_children():
        row = []
        for value in Main_Tree.item(line)['values']:
            row.append(value)
        param.append(row)
    Book.update()
    File_Name = simpledialog.askstring("File Name", "Enter the File Name")
    if File_Name == None:
        return
    else:
        f = open("C:\\Users\\" + USERNAME + "\\Desktop\\" + File_Name + ".csv","x",newline="")
        writer = csv.writer(f)

        #write the headers
        writer.writerow(Main_Tree['columns'])
        for record in param:
            writer.writerow(record)
        f.close()
        
    return