from tkinter import W

def Main_Tree_5(Tree):
    
    #Define Our Columns
    Tree['columns'] = ("Tote","WO#","SO#","PL#","Qty")
    
    # Format Our Columns
    Tree.column("#0", width = 0, minwidth = 0, stretch = False)
    Tree.column("Tote", anchor= W, width = 100, stretch = False)
    Tree.column("WO#", anchor= W, width= 100, stretch = False)
    Tree.column("SO#", anchor= W, width = 100, stretch = False)
    Tree.column("PL#", anchor= W, width = 100, stretch = False)
    Tree.column("Qty", anchor= W, width = 100, stretch = False)
    
    #Create Headings
    Tree.heading("#0", text = "", anchor = W)
    Tree.heading("Tote", text = "Tote ID", anchor = W)
    Tree.heading("WO#", text = "Work Order #", anchor = W)
    Tree.heading("SO#", text = "Sales Order #", anchor = W)
    Tree.heading("PL#", text = "Pack List #", anchor = W)
    Tree.heading("Qty", text = "Quantity", anchor = W)
    
    return