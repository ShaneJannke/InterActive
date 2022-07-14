import numpy as np
import pyodbc
from functools import partial
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees
import Sub_Log_Files
import Task_Manager

def TM_Start(Main_Tree, Book, frame6, Report_Text, Sub_Request_V, root,TM_Options_V,ME_clicked):

    root.title('Inter-Active 1.8.2/Task_Manager')

    Book.hide(1)
    Book.hide(2)
    Book.hide(3)
    Book.hide(4)
    Book.hide(5)
    Book.hide(7)
    Book.add(frame6, text=" ME ")
    '''
    6/9/22 SJ
    Automatically select the ME tab when Task Manager button is pressed
    '''
    Book.select(6)
    
    Main_Tree.bind('<ButtonRelease-1>', partial(Sub_Log_Files.selectItem,Main_Tree,Sub_Request_V))

    #call the more_info commmand when request is double clicked
    Main_Tree.bind('<Double-Button-1>', partial(Task_Manager.TM_More_Info,Report_Text, Sub_Request_V))

    Sub_Request_V.set(None)

    Task_Manager.TM_populate_status(Main_Tree,TM_Options_V,Report_Text,ME_clicked)

    return

