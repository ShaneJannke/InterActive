from tkinter import W

#README 5/16/2022 NS - This tree is no longer used

def Main_Tree_4(Tree):
    
    #Define Our Columns
    Tree['columns'] = ("Date_Add","Add_By","PN","Descript","Mfgr","Mfgr_PN","Current_Qty","SONO","WONO","PCBA","PCBA_REV","Cust","Name","Cust_PN","Cust_REV","Need_By_Date","Qty_Needed","Ref_Des","_Status","Alt_PN")
    
    # Format Our Columns
    Tree.column("#0", width=0, minwidth = 50, stretch = False)
    Tree.column("Date_Add", anchor= W, width = 100, stretch = False)
    Tree.column("Add_By", anchor= W, width = 150, stretch = False)
    Tree.column("PN", anchor= W, width = 100, stretch = False)
    Tree.column("Descript", anchor= W, width = 220, stretch = False)
    Tree.column("Mfgr_PN", anchor= W, width=160, stretch = False)
    Tree.column("Mfgr", anchor= W, width=120, stretch = False)
    Tree.column("Current_Qty", anchor= W, width=100, stretch = False)
    Tree.column("SONO", anchor= W, width = 100, stretch = False)
    Tree.column("WONO", anchor= W, width = 120, stretch = False)
    Tree.column("PCBA", anchor= W, width = 120, stretch = False)
    Tree.column("PCBA_REV", anchor= W, width = 120, stretch = False)
    Tree.column("Cust", anchor= W, width = 200, stretch = False)
    Tree.column("Name", anchor= W, width = 200)
    Tree.column("Cust_PN", anchor= W, width = 200, stretch = False)
    Tree.column("Cust_REV", anchor= W, width = 120, stretch = False)
    Tree.column("Need_By_Date", anchor= W, width = 150, stretch = False)
    Tree.column("Qty_Needed", anchor= W, width = 120, stretch = False)
    Tree.column("Ref_Des", anchor= W, width = 140, stretch = False)
    Tree.column("_Status", anchor= W, width = 120, stretch = False)
    Tree.column("Alt_PN", anchor= W, width = 200, stretch = False)
    
    #Create Headings
    Tree.heading("#0", text = "", anchor = W)
    Tree.heading("Date_Add", text = "Date_Added", anchor = W)
    Tree.heading("Add_By", text = "Added_By", anchor = W)
    Tree.heading("Descript", text = "Part Description", anchor = W)
    Tree.heading("PN", text = "Part Number", anchor = W)
    Tree.heading("Mfgr", text = "Part Manufacturer", anchor = W)
    Tree.heading("Mfgr_PN", text = "Manufacturer Part Number", anchor = W)
    Tree.heading("Current_Qty", text = "Current Quantity", anchor = W)
    Tree.heading("SONO", text = "Sales Order", anchor = W)
    Tree.heading("WONO", text = "Work Order", anchor = W)
    Tree.heading("PCBA", text = "PCBA Number", anchor = W)
    Tree.heading("PCBA_REV", text = "PCBA REV", anchor = W)
    Tree.heading("Cust", text = "Customer", anchor = W)
    Tree.heading("Name", text = "PCBA Name", anchor = W)
    Tree.heading("Cust_PN", text = "Customer Part Number", anchor = W)
    Tree.heading("Cust_REV", text = "Customer REV", anchor = W)
    Tree.heading("Need_By_Date", text = "Date Needed By", anchor = W)
    Tree.heading("Qty_Needed", text = "Quantity Needed", anchor = W)
    Tree.heading("Ref_Des", text = "Reference Designator", anchor = W)
    Tree.heading("_Status", text = "Alternate Status", anchor = W)
    Tree.heading("Alt_PN", text = "Alternate Part Number", anchor = W)
    
    return