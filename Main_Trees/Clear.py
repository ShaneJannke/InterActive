def Clear_Main_Tree(Main_Tree):
        
        Main_Tree.delete(*Main_Tree.get_children())
        
        return