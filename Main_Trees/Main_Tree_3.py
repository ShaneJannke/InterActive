from tkinter import W


def Main_Tree_3(Tree):
    
    #Define Our Columns
    Tree['columns'] = ("SN","WO#","ID","PL","Date")
    
    # Format Our Columns
    Tree.column("#0", width = 0, minwidth = 0, stretch = False)
    Tree.column("SN", anchor= W, width = 100, stretch = False)
    Tree.column("WO#", anchor= W, width=100, stretch = False)
    Tree.column("ID", anchor= W, width = 100, stretch = False)
    Tree.column("PL", anchor= W, width = 100, stretch = False)
    Tree.column("Date", anchor= W, width = 120, stretch = False)
    
    #Create Headings
    Tree.heading("#0", text = "", anchor = W)
    Tree.heading("SN", text = "Serial Number", anchor = W)
    Tree.heading("WO#", text = "Work Order", anchor = W)
    Tree.heading("ID", text = "Tote ID", anchor = W)
    Tree.heading("PL", text = "Packlist #", anchor = W)
    Tree.heading("Date", text = "Ship Date", anchor = W)
    
    return 