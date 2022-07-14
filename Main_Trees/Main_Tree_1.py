from tkinter import W

def Main_Tree_1(Tree):
    
    #Define Our Columns
    Tree['columns'] = ("Date","ID","SN","ADDED_BY")
    
    # Format Our Columns
    Tree.column("#0", width = 0, minwidth = 0, stretch = False)
    Tree.column("Date", anchor= W, width = 200, stretch = False)
    Tree.column("ID", anchor= W, width=100, stretch = False)
    Tree.column("SN", anchor= W, width = 100, stretch = False)
    Tree.column("ADDED_BY", anchor= W, width = 200, stretch = False)
    
    #Create Headings
    Tree.heading("#0", text = "", anchor = W)
    Tree.heading("Date", text = "Date", anchor = W)
    Tree.heading("ID", text = "Box ID", anchor = W)
    Tree.heading("SN", text = "Serial Number", anchor = W)
    Tree.heading("ADDED_BY", text = "Added By", anchor = W)
    
    return