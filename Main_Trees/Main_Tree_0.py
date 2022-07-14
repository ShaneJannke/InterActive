from tkinter import W

def Main_Tree_0(Tree):
    
    #Define Our Columns
    Tree['columns'] = ("A","B","C","D")
    
    # Format Our Columns
    Tree.column("#0", width = 0, minwidth = 0, stretch = False)
    Tree.column("A", anchor= W, width = 163, stretch = False)
    Tree.column("B", anchor= W, width=163, stretch = False)
    Tree.column("C", anchor= W, width = 163, stretch = False)
    Tree.column("D", anchor= W, width = 163, stretch = False)

    
    #Create Headings
    Tree.heading("#0", text = "", anchor = W)
    Tree.heading("A", text = "A", anchor = W)
    Tree.heading("B", text = "B", anchor = W)
    Tree.heading("C", text = "C", anchor = W)
    Tree.heading("D", text = "D", anchor = W)