from tkinter import W


def Main_Tree_2(Tree):
    
    #Define Our Columns
    Tree['columns'] = ("Date","WO#","SN")
    
    # Format Our Columns
    Tree.column("#0", width = 0, minwidth = 0)
    Tree.column("Date", anchor= W, width = 200)
    Tree.column("WO#", anchor= W, width= 100)
    Tree.column("SN", anchor= W, width = 100)
    
    #Create Headings
    Tree.heading("#0", text = "", anchor = W)
    Tree.heading("Date", text = "Date", anchor = W)
    Tree.heading("WO#", text = "Work Order", anchor = W)
    Tree.heading("SN", text = "Serial Number", anchor = W)
    
    return