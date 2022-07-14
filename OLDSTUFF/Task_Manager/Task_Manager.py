import numpy as np
import pyodbc
from functools import partial
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED
import Main_Trees
import Sub_Log_Files
import Task_Manager

def Task_Manager_Start(Main_Tree, Book, frame6, Report_Text, Sub_Request_V, root,ME_clicked):

    root.title('Inter-Active 1.8.0/Task_Manager')

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

    Main_Tree.bind('<Double-Button-1>', partial(Task_Manager.MoreInfo,Report_Text, Sub_Request_V))

    Sub_Request_V.set(None)

    Task_Manager.TM_populate_resp(Main_Tree,ME_clicked,Report_Text)

    return

