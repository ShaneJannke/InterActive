from tkinter import W

def Main_Tree_7(Tree):
    
    #Define Our Columns
    Tree['columns'] = ("PCBA","PCBA_REV","Bare_PCB","PCB_REV","Stencil_Need_Order","Start_Date",
                        "Feedback","PCBA_Doc","PCBA_Doc_REV")
    
    # Format Our Columns
    Tree.column("#0", width=20, stretch = False)
    Tree.column("PCBA", anchor= W, width = 70, stretch = False)
    Tree.column("PCBA_REV", anchor= W, width = 75, stretch = False)
    Tree.column("Bare_PCB", anchor= W, width = 70, stretch = False)
    Tree.column("PCB_REV", anchor= W, width= 80, stretch = False)
    Tree.column("Stencil_Need_Order", anchor= W, width = 120, stretch = False)
    Tree.column("Start_Date", anchor= W, width = 75, stretch = False)
    Tree.column("Feedback", anchor= W, width = 90, stretch = False)
    Tree.column("PCBA_Doc", anchor= W, width = 90, stretch = False)
    Tree.column("PCBA_Doc_REV", anchor= W, width = 90, stretch = False)



    #Create Headings
    Tree.heading("#0", text = "", anchor = W)
    Tree.heading("PCBA", text = "PCBA#", anchor = W)
    Tree.heading("PCBA_REV", text = "PCBA REV", anchor = W)
    Tree.heading("Bare_PCB", text = "Bare PCB#", anchor = W)
    Tree.heading("PCB_REV", text = "Bare PCB REV", anchor = W)
    Tree.heading("Stencil_Need_Order", text = "Stencil_Need_Order", anchor = W)
    Tree.heading("Start_Date", text = "Start Date", anchor = W)
    Tree.heading("Feedback", text = "Prod Feedback", anchor = W)
    Tree.heading("PCBA_Doc", text = "PCBA_Doc", anchor = W)
    Tree.heading("PCBA_Doc_REV", text = "PCBA_Doc_REV", anchor = W)

    return Tree