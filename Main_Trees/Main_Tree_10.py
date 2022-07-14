from tkinter import W

def Main_Tree_10(Tree):
    
    '''
    6/7/22 SJ
    Removed PO_PLACED_BY, as it is now stored in the change log
    Adjusted the width of some columns to save on space
    '''

    #Define Our Columns
    Tree['columns'] = ("Alt_PN","Mfgr","Mfgr_PN","Cust","PCBA","PCBA_REV")
    
    # Format Our Columns
    Tree.column("#0", width=20, stretch = False)
    Tree.column("Alt_PN", anchor= W, width = 197, stretch = False)
    Tree.column("Mfgr", anchor= W, width=200, stretch = False)
    Tree.column("Mfgr_PN", anchor= W, width=200, stretch = False)
    Tree.column("Cust", anchor= W, width = 300, stretch = False)
    Tree.column("PCBA", anchor= W, width = 120, stretch = False)
    Tree.column("PCBA_REV", anchor= W, width = 100, stretch = False)      

    #Create Headings
    Tree.heading("#0", text = "", anchor = W)
    Tree.heading("Alt_PN", text = "Part Number", anchor = W)
    Tree.heading("Mfgr", text = "Part Manufacturer", anchor = W)
    Tree.heading("Mfgr_PN", text = "Manufacturer Part Number", anchor = W)
    Tree.heading("Cust", text = "Customer", anchor = W)
    Tree.heading("PCBA", text = "PCBA Number", anchor = W)
    Tree.heading("PCBA_REV", text = "PCBA REV", anchor = W)

    return