import pywintypes
#import cd /c/win32api
from functools import partial
import numpy as np
import csv
import os
import uuid
import pyodbc
from tkinter import Tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import StringVar
from tkinter import OptionMenu
from tkinter import WORD
from tkinter import Text
from tkinter import END
from tkinter import Scrollbar
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import VERTICAL
'''
6/10/22 SJ
Commenting out this function as it was causing issues for Joe Roth - can look into possibly using a password instead
from Get_User_Dept import Get_User_Dept
'''

#Runs the init file in each of these folders, open init files to see what files are being imported
import Main_Trees
#import Task_Manager
import Sub_Log_Files
import Materials
import Feedback


class InterActive():
    def __init__(self,root):   
        '''
        6/9/22 SJ
        commenting out these variables as I do not believe they are actually used
        self.width_value = root.winfo_screenwidth()
        self.height_value = root.winfo_screenheight()
        '''
        root.title('Inter-Active 1.8.2')
        root.iconbitmap('S:\\_ENG_MANUFACTURING\\Applications\\Inter-Active\\Launcher\\Icon.ico')
        #increased width to fit more widgets in sublog
        root.geometry("1450x550")
        root.columnconfigure(0, weight=1)
        
        #X = 970
        #Y = 120
        X = 2000
        Y = 1050    
        
        self.Report_Frame_Width = 300
        self.Report_Frame_Height = 425
        self.Report_Frame = Frame(root, width = self.Report_Frame_Width, height = self.Report_Frame_Height)
        self.Book = ttk.Notebook(root, width = X)
    
        #File
        self.frame0 = Frame(self.Book, width = X, height = Y)
        #Ultratec/Production
        self.frame1 = Frame(self.Book, width = X, height = Y)
        #Ultratec/ME
        self.frame2 = Frame(self.Book, width = X, height = Y)
        #Ultratec/Materials
        self.frame3 = Frame(self.Book, width = X, height = Y)
        #Labels/Materials
        self.frame4 = Frame(self.Book, width = X, height = Y)
        #Sub Log Supply Chain
        self.frame5 = Frame(self.Book, width = X, height = Y)
        #Task Manager
        self.frame6 = Frame(self.Book, width = X, height = Y)
        #Sub Log/CSA
        self.frame7 = Frame(self.Book, width = X, height = Y)
        
        self.Main_Tree_Frame_Width = 655
        self.Main_Tree_Frame_Height = 425
        self.Main_Tree_Frame = Frame(root, width = self.Main_Tree_Frame_Width, height = self.Main_Tree_Frame_Height)
        self.Main_Tree_Frame.columnconfigure(0, weight=1)
        
        self.Tote_List = ['P#######']
        
        self.WONO_V = StringVar()
        self.WONO_V.set(0000)
        
        self.Tote_Cap = StringVar()
        self.Tote_Cap.set(0)
        
        self.Tote_Label_Count_V = StringVar()
        self.Tote_Label_Count_V.set(0)
        
        self.SN_Label_Count_V = StringVar()  
        self.SN_Label_Count_V.set(0) 

        self.Tote_Drop_V = StringVar()
        self.Tote_Drop_V.set(self.Tote_List[0])
        self.Tote_Drop_V.trace("w",self.callback)
        
        #also used in task manager for now - planning to redo task manager with new variable and layout in the future
        self.Sub_Request_V = StringVar()
        self.Sub_Request_V.set(None)     
        '''
        6/8/22 SJ
        Select Customer Reponse changed to Select Customer Responded
        Also update sub_request_populate and Sub_Change_Status
        Update entries in database that currently have status of Customer Reponse
        -- RUN THIS SQL TO UPDATE--
        UPDATE Testdatabase.dbo.sub_request
        SET _STATUS = 'Customer Responded'
        WHERE _STATUS = 'Customer Response'

        6/10/22 SJ
        Open changed to Select Pending SC
        '''

        #list of status' to sort the sublog by
        self.Sub_Options = ['Select Initiated','Select Pending SC','Select Pending ME','Select Pending CAS','Select Pending Customer','Select Customer Responded',"Select PO Needed",'Select Closed']
        self.Sub_Options_V = StringVar()
        self.Sub_Options_V.set(self.Sub_Options[0])

        self.WO_Options = ['Select All','Select Assigned','Select Unassigned','Select Scrap']
        self.WO_Options_V = StringVar()
        self.WO_Options_V.set(self.WO_Options[0])  

        self.WO_SN_Count_V = StringVar()  
        self.WO_SN_Count_V.set(0)      

        self.WO_SN_V = StringVar()
        self.WO_SN_V.set(0000)  

        #list of status' to sort the Task Manager by
        #self.TM_Options = ['Select Initiated','Select Open','Select In Progress','Select Pending Review','Select Rejected','Select Closed']
        #self.TM_Options_V = StringVar()
        #self.TM_Options_V.set(self.TM_Options[0])

        '''
        6/8/22 SJ
        Creates a list of ME users for the Task Manager
        '''
        #ME_names = Task_Manager.TM_Get_Names()
        #self.ME_clicked = StringVar()
        #self.ME_clicked.set(ME_names[0])
        '''
        6/8/22 SJ
        Creates a list of Users for the Sub Log
        '''
        Sub_names = Sub_Log_Files.Get_Sub_Names()
        self.Sub_clicked = StringVar()
        self.Sub_clicked.set(Sub_names[0])

        '''
        6/7/22 SJ
        Runs the function to pull department of active user.
        Used to determine Program permissions - See Sub_Log, Ultratec, Task_Manager, Label_Printing  functions.
        6/10/22 SJ
        commenting this out as it was causing errors for Joe Roth - can look into another method to achieve this later
        '''
        #self.DEPT = Get_User_Dept()
       #-------------------------------------------------------------------------------------------------------------------------------------- 
        #Report Frame Widgets
        '''
        6/9/22 SJ
        Report_Text needs to be disabled upon creation
        '''
        self.Report_Text = Text(self.Report_Frame, width = 33, height = 14, wrap = WORD, spacing3 = 10, state=DISABLED)
        self.Report_Scroll = Scrollbar(self.Report_Frame, orient = "vertical",command = self.Report_Text.yview)
        
        #Create a Clear Report Text Button
        self.Clear_Report_B = Button(self.Report_Frame, text="Clear", command= self.Clear_Report)
        #-------------------------------------------------------------------------------------------------------------------------------------------------
        #Main Tree Frame Widgets
        '''
        6/8/22 SJ
        Main_Tree.bind moved to Sub_Log function, allows for different bindings for different programs (Task Manager, etc)
        binding will only occur after sub log button has been pressed, so if it needed for ultratec this can be reverted
        '''
        self.Main_Tree = ttk.Treeview(self.Main_Tree_Frame, height = 17)
     
        self.Main_Tree_Scroll_Y = Scrollbar(self.Main_Tree_Frame, orient = "vertical", command = self.Main_Tree.yview)
        self.Main_Tree_Scroll_X = Scrollbar(self.Main_Tree_Frame, orient = "horizontal", command = self.Main_Tree.xview)
        
        # Create striped row tags
        self.Main_Tree.tag_configure('PrimaryRow', background = "lightgrey")
        
        # Create striped row tags
        self.Main_Tree.tag_configure('SecondaryRow', background = "powderblue")

        #Create a Clear Button to clear the treeview
        #self.Clear_Main_Tree_B = Button(self.Main_Tree_Frame, text="Clear Data", command= self.Clear_Main_Tree)
        self.Clear_Main_Tree_B = Button(self.Main_Tree_Frame, text="Clear Data", command= partial(Main_Trees.Clear_Main_Tree,self.Main_Tree))
        
        #Create an Export Button to export a csv file
        self.Export_Main_Tree_B = Button(self.Main_Tree_Frame, text="Export.csv", command= partial(Main_Trees.Export_Main_Tree,self.Main_Tree,self.Book))
        #--------------------------------------------------------------------------------------------------------------------------------------
        #File Frame 0 Widgets
        '''
        6/7/22  SJ
        Functions must be passed root so they can update root.title to show the current selected program.
        '''
        self.Ultratec_B = Button(self.frame0, text = "Ultratec", command = lambda: self.Ultratec(root))
        #6/15/22 SJ - changed text to Materials to be more generic as we add more functions
        self.Label_Printing_B = Button(self.frame0, text = "Materials", command = lambda: self.Label_Printing(root))
        
        self.Sub_Log_B = Button(self.frame0, text = "Sub Log", command = lambda: self.Sub_Log(root))

        self.Task_Manager_B = Button(self.frame0)

        self.frame0_Separator_Label_1 = Label(self.frame0, text = "Programs", font = "arial 10 bold")
        self.frame0_Separator_1 = ttk.Separator(self.frame0, orient = VERTICAL)

        '''
        6/9/22 SJ
        Create buttons to submit and view overall feedback for interactive
        '''
        self.Submit_Feedback_B = Button(self.frame0, text= "Submit Feedback", command = partial(Feedback.Submit_Feedback,self.Report_Text))

        self.Get_Feedback_B = Button(self.frame0, text= "View Feedback", command = partial(Feedback.Get_Feedback,self.Report_Text))

        self.Edit_Feedback_B = Button(self.frame0, text= "Edit Feedback", command = partial(Feedback.Edit_Feedback,self.Report_Text))

        self.frame0_Separator_Label_2 = Label(self.frame0, text = "InterActive Feedback", font = "arial 10 bold")
        self.frame0_Separator_2 = ttk.Separator(self.frame0, orient = VERTICAL)

        #------------------------------------------------------------------------------------------------------------------------------------------------
        #Frame 1 Widgets Ultratec/Production
        
        self.WO_Tote_B = Button(self.frame1, text = "Add WO#", command = self.WO_Tote)
        
        self.WONO_Text_Label = Label(self.frame1,text = "WO#:", font = "arial 10")
        self.WONO_Text = Label(self.frame1, textvariable = self.WONO_V, font = "arial 10")

        self.frame1_Separator_Label_1 = Label(self.frame1, text = "Work Order", font = "arial 10 bold")
        self.frame1_Separator_1 = ttk.Separator(self.frame1, orient = VERTICAL)
        
        self.SN_To_Tote_B = Button(self.frame1, text="Scan Part", command= self.SN_To_Tote)
        
        self.Tote_SN_B = Button(self.frame1, text="Add Tote(s)", command= self.Tote_SN)
         
        self.Totelabel = Label(self.frame1, text = "Current Tote(s) in Queue:", font="arial 10")
        self.Tote_Label_Count = Label(self.frame1, textvariable= self.Tote_Label_Count_V, font="arial 10")
        
        self.SNlabel = Label(self.frame1, text = "Current SNs Scanned:", font="arial 10")
        self.SNlabelCount = Label(self.frame1, textvariable= self.SN_Label_Count_V, font="arial 10")

        self.frame1_Separator_Label_2 = Label(self.frame1, text = "Tote Queue", font = "arial 10 bold")
        self.frame1_Separator_2 = ttk.Separator(self.frame1, orient = VERTICAL)
        
        self.New_Tote_ID_B = Button(self.frame1, text="New Tote ID", command= self.New_Tote_ID)
        
        self.Utec_Label_Print_B = Button(self.frame1, text = "Print Tote ID", command = self.Utec_Label_Print)
        
        self.Tote_Drop = OptionMenu(self.frame1, self.Tote_Drop_V, *self.Tote_List)

        self.frame1_Separator_Label_3 = Label(self.frame1, text = "Tote ID", font = "arial 10 bold")
        self.frame1_Separator_3 = ttk.Separator(self.frame1, orient = VERTICAL)
           
        self.Remove_SN_From_Tote_B = Button(self.frame1, text="Delete SN", command= self.Remove_SN_From_Tote)
        
        self.Delete_Tote_B = Button(self.frame1, text="Delete Tote ID", command= self.Delete_Tote)

        self.frame1_Separator_Label_4 = Label(self.frame1, text = "SN/Tote Control", font = "arial 10 bold")
        self.frame1_Separator_4 = ttk.Separator(self.frame1, orient = VERTICAL)

        self.SN_Info_B = Button(self.frame1, text = "View 1 SN", command = self.SN_Info)

        self.frame1_Separator_Label_5 = Label(self.frame1, text = "View SN", font = "arial 10 bold")
        self.frame1_Separator_5 = ttk.Separator(self.frame1, orient = VERTICAL) 

        #------------------------------------------------------------------------------------------------------------------------------------------------
        #Frame 2 Widgets Ultratec/ME
        '''
        6/7/22 SJ
        WO_Options and WO_Options_V moved toward the top where the other variables are created, for consistency.
        '''
        self.WO_Options_Menu = OptionMenu(self.frame2, self.WO_Options_V, *self.WO_Options)
        self.WO_Options_V.trace("w",self.callback2)

        self.WO_SN_B = Button(self.frame2, text = "Add WO#", command = self.WO_SN)

        self.WO_SN_Label = Label(self.frame2, text = "Serial Number Count:", font="arial 10")
        self.WO_SN_Count = Label(self.frame2, textvariable= self.WO_SN_Count_V, font="arial 10")
        '''
        6/7/22 SJ
        WO_SN_Count_V moved up top by other variables.
        WO_SN_V moved up top by other variables.
        '''      
        self.WO_SN_Text_Label = Label(self.frame2,text = "WO#:", font = "arial 10")
        self.WO_SN_Text = Label(self.frame2, textvariable = self.WO_SN_V, font = "arial 10")

        self.frame2_Separator_Label_1 = Label(self.frame2, text = "Work Order", font = "arial 10 bold")
        self.frame2_Separator_1 = ttk.Separator(self.frame2, orient = VERTICAL)
        
        self.Delete_All_SNs_From_WO_B = Button(self.frame2, text = "Delete All SN's", command = self.Delete_All_SNs_From_WO)
        
        self.Import_SN_B = Button(self.frame2, text = "Import SN's", command = self.Import_SN)

        self.View_Last_SN_B = Button(self.frame2, text = "View Last SN", command = self.View_Last_SN)
          
        self.Q_Tote_Summary_B = Button(self.frame2, text = "Tote Summary", command = self.Q_Tote_Summary)
        
        self.frame2_Separator_Label_2 = Label(self.frame2, text = "SN Control", font = "arial 10 bold")
        self.frame2_Separator_2 = ttk.Separator(self.frame2, orient = VERTICAL)
        
        self.W_SN_To_Scrap_B = Button(self.frame2, text = "Scrap SN", command = self.W_SN_To_Scrap)

        self.Q_Check_For_Issues_B = Button(self.frame2, text = "Manex/Interactive\n Report", command = self.Q_Check_For_Issues)
        
        self.frame2_Separator_Label_4 = Label(self.frame2, text = "SN Scrap", font = "arial 10 bold")
        self.frame2_Separator_4 = ttk.Separator(self.frame2, orient = VERTICAL)       
        #------------------------------------------------------------------------------------------------------------------------------------------------
        #Frame 3 Widgets aka Ultratec/Materials
        '''
        6/8/22 SJ
        Add_Pl_Get_Cust_View_B text changed to Generate CSV/Packlist
        Q_PL_Report_B text changed to Export Packlist Report
        '''
        self.Add_Pl_Get_Cust_View_B = Button(self.frame3, text="Generate CSV/Packlist", command= self.Add_Pl_Get_Cust_View)
        
        self.Q_PL_Report_B = Button(self.frame3, text = "Re-Export Packlist Report", command = self.Q_PL_Report)
              
        self.frame3_Separator_Label_1 = Label(self.frame3, text = "Reports", font = "arial 10 bold")
        self.frame3_Separator_1 = ttk.Separator(self.frame3, orient = VERTICAL)
               
        self.Tote_SN_B_3 = Button(self.frame3, text="Add Tote(s)", command= self.Tote_SN)
         
        self.Totelabel_3 = Label(self.frame3, text = "Current Tote(s) in Queue:", font="arial 10")
        self.Tote_Label_Count_3 = Label(self.frame3, textvariable= self.Tote_Label_Count_V, font="arial 10")
        
        self.SNlabel_3 = Label(self.frame3, text = "Current SNs Scanned:", font="arial 10")
        self.SNlabelCount_3 = Label(self.frame3, textvariable= self.SN_Label_Count_V, font="arial 10")

        self.frame3_Separator_Label_2 = Label(self.frame3, text = "Tote Queue", font = "arial 10 bold")
        self.frame3_Separator_2 = ttk.Separator(self.frame3, orient = VERTICAL)      
        #------------------------------------------------------------------------------------------------------------------------------------------------
        #Frame 4 Widgets Label/Materials

        self.Update_WO_SN_For_Labels = Button(self.frame4, text="Print Labels", command= partial(Materials.Update_WO_SN_For_Labels,self.Book,self.Report_Text))

        #self.Utec_W_Update_SN_Labels_B = Button(self.frame4, text="Print Ultratec\nLabels", command= self.Utec_W_Update_SN_Labels)
        
        self.frame4_Separator_Label_1 = Label(self.frame4, text = "Labels", font = "arial 10 bold")
        self.frame4_Separator_1 = ttk.Separator(self.frame4, orient = VERTICAL)   
        #------------------------------------------------------------------------------------------------------------------------------------------------
        #Frame 5 Widgets Sub Log/Supply Chain     
        self.New_Sub_Request_B = Button(self.frame5, text = "New Sub \nRequest", command = partial(Sub_Log_Files.New_Sub_Request,self.Main_Tree,self.Sub_Request_V,self.Report_Text,self.Book))

        self.frame5_Separator_Label_1 = Label(self.frame5, text = "New", font = "arial 10 bold")
        self.frame5_Separator_1 = ttk.Separator(self.frame5, orient = VERTICAL)

        self.Sub_Request_Text_Label = Label(self.frame5,text = "Sub Request #:", font = "arial 10")
        self.Sub_Request_Text = Label(self.frame5, textvariable = self.Sub_Request_V, font = "arial 10")

        self.Sub_By_WONO_B = Button(self.frame5, text = "Add by WO#", command = partial(Sub_Log_Files.Sub_By_WONO,self.Report_Text,self.Sub_Request_V,self.Main_Tree,self.Book))
        
        self.Sub_By_SONO_B = Button(self.frame5, text = "Add by SO#", command = partial(Sub_Log_Files.Sub_By_SONO,self.Sub_Request_V,self.Main_Tree,self.Book,self.Report_Text))
        
        self.Sub_Add_PO_B = Button(self.frame5, text = "Add PO#", command = partial(Sub_Log_Files.Sub_Add_PO,self.Sub_Request_V,self.Report_Text,self.Main_Tree,self.Book))

        self.Sub_Add_Alt_B = Button(self.frame5, text = "Add Alternate", command = partial(Sub_Log_Files.Sub_Add_Alt,self.Main_Tree,self.Sub_Options_V,self.Sub_Request_V,self.Report_Text,self.Sub_clicked,self.Book))

        self.frame5_Separator_Label_2 = Label(self.frame5, text = "Add", font = "arial 10 bold")
        self.frame5_Separator_2 = ttk.Separator(self.frame5, orient = VERTICAL)
      
        self.Sub_Options_Menu = OptionMenu(self.frame5, self.Sub_Options_V, *self.Sub_Options)
        self.Sub_Options_V.trace("w",self.callback3)

        self.View_Sub_Request_B = Button(self.frame5, text = "View Sub \nRequest", command = partial(Sub_Log_Files.View_Sub_Request,None,self.Main_Tree,self.Book,self.Sub_Request_V,self.Report_Text))

        self.Sub_View_By_WONO_B = Button(self.frame5, text = "View by WONO", command = partial(Sub_Log_Files.Sub_View_By_WONO,self.Main_Tree,self.Book,self.Report_Text))

        self.Sub_View_By_PN_B = Button(self.frame5, text = "View by PN", command = partial(Sub_Log_Files.Sub_View_By_PN,self.Main_Tree,self.Book,self.Report_Text))

        self.frame5_Separator_Label_3 = Label(self.frame5, text = "View", font = "arial 10 bold")
        self.frame5_Separator_3 = ttk.Separator(self.frame5, orient = VERTICAL)

        self.Sub_Remove_Request_B = Button(self.frame5, text = "Delete Request", command = partial(Sub_Log_Files.Sub_Remove_Request,self.Sub_Request_V,self.Report_Text,self.Main_Tree,self.Sub_Options_V,self.Sub_clicked))

        self.Sub_Remove_By_PN_B = Button(self.frame5, text = "Remove PN", command = partial(Sub_Log_Files.Sub_Remove_By_PN,self.Sub_Request_V,self.Book,self.Report_Text,self.Main_Tree,self.Sub_Options_V,self.Sub_clicked))
        
        self.frame5_Separator_Label_4 = Label(self.frame5, text = "Remove", font = "arial 10 bold")
        self.frame5_Separator_4 = ttk.Separator(self.frame5, orient = VERTICAL)

        self.Sub_View_Note_B = Button(self.frame5, text = "View Note", command = partial(Sub_Log_Files.Sub_View_Note,self.Sub_Request_V,self.Report_Text))
        
        self.Sub_Request_Note_B = Button(self.frame5, text = "Add Note", command = partial(Sub_Log_Files.Sub_Request_Note,self.Sub_Request_V,self.Report_Text,self.Main_Tree,self.Book))
        
        self.frame5_Separator_Label_5 = Label(self.frame5, text = "Request Note", font = "arial 10 bold")
        self.frame5_Separator_5 = ttk.Separator(self.frame5, orient = VERTICAL)

        self.Sub_Change_Status_B = Button(self.frame5, text = "Change Status", command = partial(Sub_Log_Files.Sub_Change_Status,self.Sub_Request_V,self.Report_Text,self.Main_Tree,self.Book))

        self.Supply_Chain_Sub_Report_B = Button(self.frame5, text = "Sub Request\nReport", command = partial(Sub_Log_Files.Supply_Chain_Sub_Report,self.Sub_Request_V,self.Report_Text))

        #output the changelog into the report frame
        self.Sub_Change_Log_B = Button(self.frame5, text="Change Log",command=partial(Sub_Log_Files.Sub_View_Change_Log,self.Sub_Request_V,self.Report_Text))

        self.frame5_Separator_Label_6 = Label(self.frame5, text = "Status", font = "arial 10 bold")
        self.frame5_Separator_6 = ttk.Separator(self.frame5, orient = VERTICAL)

        #Dropdown list of Users
        self.Sub_Users_Drop = OptionMenu(self.frame5, self.Sub_clicked, *Sub_names)
        self.Sub_clicked.trace("w",self.callback4)

        #Opens a window to choose the responsible party for selected Sub Request
        self.Sub_Set_Resp_B = Button(self.frame5, text="Set Resp Party",command=partial(Sub_Log_Files.Sub_Set_Resp_Party,self.Sub_clicked,self.Sub_Request_V,self.Main_Tree,self.Report_Text,self.Sub_Options_V,self.Book))

        #returns responsible parties per department in report frame
        self.Sub_Get_Resp_B = Button(self.frame5, text="Get Resp Party",command=partial(Sub_Log_Files.Sub_Get_Resp_Party,self.Sub_Request_V,self.Report_Text))
        
        self.frame5_Separator_Label_7 = Label(self.frame5, text = "Responsible Party", font = "arial 10 bold")
        self.frame5_Separator_7 = ttk.Separator(self.frame5, orient = VERTICAL)

        self.Sub_Change_QTY_B = Button(self.frame5, text = "Change QTY \nNeeded", command = partial(Sub_Log_Files.Sub_Change_QTY_Needed,self.Report_Text,self.Sub_Request_V,self.Main_Tree,self.Sub_Options_V,self.Sub_clicked,self.Book))

        self.Sub_Alt_History_B = Button(self.frame5, text="PN Alt History", command=partial(Sub_Log_Files.Sub_Alt_History,self.Main_Tree,self.Report_Text,self.Book))
   
        self.Sub_Where_Alt_Used_B = Button(self.frame5, text="Where Alt Used", command=partial(Sub_Log_Files.Sub_Where_Alt_Used,self.Main_Tree,self.Report_Text,self.Book))
        
        self.frame5_Separator_Label_8 = Label(self.frame5, text = "BOM Search", font = "arial 10 bold")
        self.frame5_Separator_8 = ttk.Separator(self.frame5, orient = VERTICAL)
        #------------------------------------------------------------------------------------------------------------------------------------------------
       #Frame 6 Widgets
        #search by assembly or rev
        self.TM_Search_Assy_B = Button(self.frame6, text = "Search Assembly")

        #search by work order number
        self.TM_Search_WO_B = Button(self.frame6, text = "Search WO#")

        self.frame6_Separator_Label_1 = Label(self.frame6, text = "Current PCBA", font = "arial 10 bold")
        self.frame6_Separator_1 = ttk.Separator(self.frame6, orient = VERTICAL)
        
        #add a note to the selected work order
        self.TM_Edit_Note_B = Button(self.frame6, text = "Edit Notes")

        #view notes for selected work order
        self.TM_View_Note_B = Button(self.frame6, text = "View Notes")
        
        self.frame6_Separator_Label_2 = Label(self.frame6, text = "Search", font = "arial 10 bold")
        self.frame6_Separator_2 = ttk.Separator(self.frame6, orient = VERTICAL)

        #view ECN/Doc Request info
        self.TM_Doc_View_B = Button(self.frame6, text = "View ECN/Doc Req ID")

        #insert ECN/ Doc Request info for selected work order
        self.TM_Doc_Insert_B = Button(self.frame6, text = "Insert ECN/Doc Req ID")

        #creates a pop-up showing the full production feedback
        self.TM_Feedback_B = Button(self.frame6, text = "Production Feedback")
        
        self.frame6_Separator_Label_3 = Label(self.frame6, text = "Notes", font = "arial 10 bold")
        self.frame6_Separator_3 = ttk.Separator(self.frame6, orient = VERTICAL)
            
        #create a dropdown list of users in ME
        #self.TM_Users_Drop = OptionMenu(self.frame6, self.ME_clicked, *ME_names)
        #self.ME_clicked.trace("w",self.callback5)

        #set selected user from dropdown responsible for selected work order
        self.TM_Set_Resp_B = Button(self.frame6, text="Set Resp Party")

        #get responsible user for selected work order
        self.TM_Get_Resp_B = Button(self.frame6, text="Get Resp Party")

        self.frame6_Separator_Label_4 = Label(self.frame6, text = "Other Info", font = "arial 10 bold") 
        self.frame6_Separator_4 = ttk.Separator(self.frame6, orient = VERTICAL)

        '''
        6/9/22 SJ
        displays the selected work order, similar to Sub Log
        '''
        self.TM_WO_Text_Label = Label(self.frame6,text = "PCBA #:", font = "arial 10")
        self.TM_WO_Text = Label(self.frame6, textvariable = self.Sub_Request_V, font = "arial 10")

        self.frame6_Separator_Label_5 = Label(self.frame6, text = "Responsible Party", font = "arial 10 bold")
        self.frame6_Separator_5 = ttk.Separator(self.frame6, orient = VERTICAL)

        self.New_TM_Request_B = Button(self.frame6, text="New Request")
        
        self.TM_Add_Assembly_B = Button(self.frame6, text="Add Assembly")
       
        self.TM_View_Request_B = Button(self.frame6, text="View Request")
        #------------------------------------------------------------------------------------------------------------------------------------------------
        #Frame 7 Widgets
        self.Kit_Label_B = Button(self.frame7, text="Kitting Label",command=partial(Materials.KittingLabel,self.Report_Text,self.Book))

        self.frame7_Separator_Label_1 = Label(self.frame7, text = "Kitting", font = "arial 10 bold")
        self.frame7_Separator_1 = ttk.Separator(self.frame7, orient = VERTICAL)
    
        self.conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                    "Server=DC01;"
                    "Database=ManexExtras;"
                    "Trusted_Connection=yes;")

        self.Construct() 
        #self.PasswordCheck(root)
        return

    def Construct(self):

        self.Book.grid(row = 0, column = 0, columnspan = 3, sticky = "w")
        
        self.frame0.grid(row = 0, column = 0)
        self.frame1.grid(row = 0, column = 0)
        self.frame2.grid(row = 0, column = 0)
        self.frame3.grid(row = 0, column = 0)
        self.frame4.grid(row = 0, column = 0)
        self.frame5.grid(row = 0, column = 0)
        self.frame6.grid(row = 0, column = 0)
        self.frame7.grid(row = 0, column = 0)
         
        self.Book.add(self.frame0, text=" File ")
        self.Book.add(self.frame1, text=" Produciton ")
        self.Book.add(self.frame2, text=" ME ")        
        self.Book.add(self.frame3, text = " Materials ")
        #6/15/22 SJ changed from Materials to Label Printing 
        self.Book.add(self.frame4, text = " Label Printing ")
        self.Book.add(self.frame5, text = " Sub Log ")
        self.Book.add(self.frame6, text = " Task Manager ")
        #6/17/22 SJ adding new tab "Kitting" to materials
        self.Book.add(self.frame7, text = " Kitting ")
        
        # Add some style, this is to enable color tags for the main tree
        self.style = ttk.Style()
        self.style.configure("Treeview",
                        background = "silver",
                        foreground = "black",
                        fieldbackground="silver"
                        )
        #Change selected color
        self.style.map('Treeview',background=[('selected','dimgrey')])

        '''
        06/06/2022 SJ
        Editted column placements to remove unnecessary gaps in numbers.
        Columnspan added to separator labels to help center them.
        Grouped related items together.
        '''
        #----------------------------------------------------------------------------------------------------------------------------------------------------
        #Frame0 aka File
        self.Ultratec_B.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.Sub_Log_B.grid(row = 1, column = 0)

        self.Label_Printing_B.grid(row = 0, column = 1, padx = 5, pady = 5, ipadx=5)

        #self.Task_Manager_B.grid(row = 1, column = 1)
        
        self.frame0_Separator_Label_1.grid(row = 2, column = 0, columnspan=2)
        self.frame0_Separator_1.grid(row = 0, column = 2, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Submit_Feedback_B.grid(row=0, column = 3, padx=5, pady=5)

        self.Get_Feedback_B.grid(row=1, column = 3, padx=5, pady=5)

        self.Edit_Feedback_B.grid(row=0, column=4)

        self.frame0_Separator_Label_2.grid(row = 2, column = 3, columnspan=2)
        self.frame0_Separator_2.grid(row = 0, column = 5, sticky = "ns", rowspan = 3, padx = 5, pady = 5)
        #---------------------------------------------------------------------------------------------------------------------------------------------
        #Frame1 aka Ultratech/Production  

        #added columnspan to center button
        self.WO_Tote_B.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan=2)
        
        self.WONO_Text_Label.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.WONO_Text.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.frame1_Separator_Label_1.grid(row = 2, column = 0, columnspan=2)
        self.frame1_Separator_1.grid(row = 0, column = 2, rowspan = 3, sticky = "ns", padx = 5, pady = 5)
        
        self.SN_To_Tote_B.grid(row = 0, column = 3)
        
        self.Tote_SN_B.grid(row = 1, column = 3)
        
        self.Totelabel.grid(row = 0, column = 4) 
        self.Tote_Label_Count.grid(row = 0, column = 5)
          
        self.SNlabel.grid(row = 1, column = 4) 
        self.SNlabelCount.grid(row = 1, column = 5)

        self.frame1_Separator_Label_2.grid(row = 2, column = 3, columnspan=3)
        self.frame1_Separator_2.grid(row = 0, column = 7, sticky = "ns", rowspan = 3, padx = 5, pady = 5)
          
        self.New_Tote_ID_B.grid(row = 0, column = 8, padx = 5, pady = 5)
        
        self.Utec_Label_Print_B.grid(row = 1, column = 8, padx = 5, pady = 5)
        
        self.Tote_Drop.grid(row = 0, column = 9, padx = 5, pady = 5)
        
        self.frame1_Separator_Label_3.grid(row = 2, column = 8, columnspan=2)
        self.frame1_Separator_3.grid(row = 0, column = 10, sticky = "ns", rowspan = 3, padx = 5, pady = 5)
            
        self.Remove_SN_From_Tote_B.grid(row = 0, column = 11) 
        
        self.Delete_Tote_B.grid(row = 1, column = 11)

        self.frame1_Separator_Label_4.grid(row = 2, column = 11)
        self.frame1_Separator_4.grid(row = 0, column = 12, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        #added rowspan to center the button
        self.SN_Info_B.grid(row = 0, column = 13, rowspan=2)

        self.frame1_Separator_Label_5.grid(row = 2, column = 13)
        self.frame1_Separator_5.grid(row = 0, column = 14, sticky = "ns", rowspan = 3, padx = 5, pady = 5)
        #---------------------------------------------------------------------------------------------------------------------------------------------
        #Frame2 aka Ultratec/ME
        self.WO_Options_Menu.grid(row = 0, column = 0, padx = 5, pady = 5)
        
        self.WO_SN_B.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.WO_SN_Label.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.WO_SN_Count.grid(row = 0, column = 2, padx = 5, pady = 5)
 
        self.WO_SN_Text_Label.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.WO_SN_Text.grid(row = 1, column = 2)
          
        self.frame2_Separator_Label_1.grid(row = 2, column = 0, padx = 5, pady = 5, columnspan=3)
        self.frame2_Separator_1.grid(row = 0, column = 3, sticky = "ns", rowspan = 3, padx = 5, pady = 5)
        
        self.Delete_All_SNs_From_WO_B.grid(row = 0, column = 4, padx = 5, pady = 5)
        
        self.Import_SN_B.grid(row = 1, column = 4, padx = 5, pady = 5)
        
        self.View_Last_SN_B.grid(row = 0, column = 5, padx = 5, pady = 5)
        
        self.Q_Tote_Summary_B.grid(row = 1, column = 5, padx = 5, pady = 5)

        self.frame2_Separator_Label_2.grid(row = 2, column = 4, columnspan=2)
        self.frame2_Separator_2.grid(row = 0, column = 6, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.W_SN_To_Scrap_B.grid(row = 0, column = 9)

        self.Q_Check_For_Issues_B.grid(row = 1, column = 9)

        self.frame2_Separator_Label_4.grid(row = 2, column = 9)
        self.frame2_Separator_4.grid(row = 0, column = 10, sticky = "ns", rowspan = 3, padx = 5, pady = 5)
        #---------------------------------------------------------------------------------------------------------------------------------------------        
        #Frame 3  Ultratec/Materials
        self.Add_Pl_Get_Cust_View_B.grid(row = 0, column = 0, padx = 5, pady = 5)
        
        self.Q_PL_Report_B.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.frame3_Separator_Label_1.grid(row = 2, column = 0)
        self.frame3_Separator_1.grid(row = 0, column = 1, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Tote_SN_B_3.grid(row = 0, column = 2, padx = 5, pady = 5) 
        
        self.Totelabel_3.grid(row = 0, column = 3, padx = 5, pady = 5)
        self.Tote_Label_Count_3.grid(row = 0, column = 4, padx = 5, pady = 5)
          
        self.SNlabel_3.grid(row = 1, column = 3, padx = 5, pady = 5)  
        self.SNlabelCount_3.grid(row = 1, column = 4, padx = 5, pady = 5)

        self.frame3_Separator_Label_2.grid(row = 2, column = 2, columnspan=3)
        self.frame3_Separator_2.grid(row = 0, column = 5, sticky = "ns", rowspan = 5, padx = 5, pady = 5)
        #---------------------------------------------------------------------------------------------------------------------------------------------
        #Frame4 aka Label/Materials  
        self.Update_WO_SN_For_Labels.grid(row = 0, column = 0, padx = 5, pady = 5)
        #self.Utec_W_Update_SN_Labels_B.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.frame4_Separator_Label_1.grid(row = 1, column = 0)
        self.frame4_Separator_1.grid(row = 0, column = 1, sticky = "ns", rowspan = 3, padx = 5, pady = 5)          
        #---------------------------------------------------------------------------------------------------------------------------------------------        
        #Frame 5 Sub Log/Supply Chain
        self.New_Sub_Request_B.grid(row = 0, column = 0, rowspan=2)

        self.frame5_Separator_Label_1.grid(row = 2, column = 0)
        self.frame5_Separator_1.grid(row = 0, column = 1, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Sub_Request_Text_Label.grid(row = 0, column = 2)
        self.Sub_Request_Text.grid(row = 0, column = 3)
        
        self.Sub_By_WONO_B.grid(row = 1, column = 2)
        
        self.Sub_By_SONO_B.grid(row = 1, column = 3, padx = 10)

        self.Sub_Add_PO_B.grid(row = 0, column = 4)

        self.Sub_Add_Alt_B.grid(row = 1, column = 4)

        self.frame5_Separator_Label_2.grid(row = 2, column = 2, columnspan=3)
        self.frame5_Separator_2.grid(row = 0, column = 5, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Sub_Options_Menu.grid(row = 0, column = 6)

        self.View_Sub_Request_B.grid(row = 1, column = 6)

        self.Sub_View_By_WONO_B.grid(row = 0, column = 7, padx = 5)

        self.Sub_View_By_PN_B.grid(row = 1, column = 7)

        self.frame5_Separator_Label_3.grid(row = 2, column = 6, columnspan=2)
        self.frame5_Separator_3.grid(row = 0, column = 8, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Sub_Remove_Request_B.grid(row = 0, column = 9)

        self.Sub_Remove_By_PN_B.grid(row = 1, column = 9)
        
        self.frame5_Separator_Label_4.grid(row = 2, column = 9)
        self.frame5_Separator_4.grid(row = 0, column = 10, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Sub_View_Note_B.grid(row = 0, column = 11)

        self.Sub_Request_Note_B.grid(row = 1, column = 11)
        
        self.frame5_Separator_Label_5.grid(row = 2, column = 11)
        self.frame5_Separator_5.grid(row = 0, column = 12, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Sub_Change_Status_B.grid(row = 0, column = 13)

        self.Supply_Chain_Sub_Report_B.grid(row = 1, column = 13)

        self.Sub_Change_Log_B.grid(row=0, column=14, padx=5, pady=5)

        self.frame5_Separator_Label_6.grid(row = 2, column = 13, columnspan=2)
        self.frame5_Separator_6.grid(row = 0, column = 15, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Sub_Users_Drop.grid(row=0, column=16, padx=5, pady=5)

        self.Sub_Set_Resp_B.grid(row=0, column=17, padx=5, pady=5)

        self.Sub_Get_Resp_B.grid(row=1, column=17, padx=5, pady=5)

        self.frame5_Separator_Label_7.grid(row = 2, column = 16, columnspan=2)
        self.frame5_Separator_7.grid(row = 0, column = 18, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.Sub_Change_QTY_B.grid(row=1, column=14, padx=5, pady=5)

        self.Sub_Alt_History_B.grid(row=0, column=19, padx=5, pady=5)

        self.Sub_Where_Alt_Used_B.grid(row = 1, column=19, padx=5, pady=5)

        self.frame5_Separator_Label_8.grid(row = 2, column = 19, columnspan=2)
        self.frame5_Separator_8.grid(row = 0, column = 20, sticky = "ns", rowspan = 3, padx = 5, pady = 5)
        #---------------------------------------------------------------------------------------------------------------------------------------------
        #Frame 6 Task Manager/Task Manager
        self.TM_WO_Text_Label.grid(row = 0, column = 0, rowspan=2)
        self.TM_WO_Text.grid(row = 0, column = 1,rowspan=2)
        
        self.frame6_Separator_Label_1.grid(row = 2, column = 0, columnspan=2)
        self.frame6_Separator_1.grid(row = 0, column = 2, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.TM_Search_Assy_B.grid(row = 0, column = 3, padx = 5, pady = 5)

        self.TM_Search_WO_B.grid(row = 1, column = 3, padx=5, pady=5, ipadx= 5)

        self.frame6_Separator_Label_2.grid(row = 2, column = 3)
        self.frame6_Separator_2.grid(row = 0, column = 4, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.TM_Edit_Note_B.grid(row = 0, column = 5)

        self.TM_View_Note_B.grid(row = 1, column = 5)

        self.frame6_Separator_Label_3.grid(row = 2, column = 5, columnspan=2)
        self.frame6_Separator_3.grid(row = 0, column = 6, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.TM_Doc_View_B.grid(row = 1, column = 7, padx=5, ipadx= 1)

        self.TM_Doc_Insert_B.grid(row = 0, column = 7)

        self.TM_Feedback_B.grid(row = 0, column = 8, padx=5)

        self.frame6_Separator_Label_4.grid(row = 2, column = 7, columnspan=2)
        self.frame6_Separator_4.grid(row = 0, column = 9, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        #self.TM_Users_Drop.grid(row=0, column=10, padx=5, pady=5)

        self.TM_Set_Resp_B.grid(row=0, column=11, padx=5, pady=5)

        self.TM_Get_Resp_B.grid(row=1, column=11, padx=5, pady=5)

        self.frame6_Separator_Label_5.grid(row = 2, column = 10, columnspan=2)
        self.frame6_Separator_5.grid(row = 0, column = 12, sticky = "ns", rowspan = 3, padx = 5, pady = 5)

        self.New_TM_Request_B.grid(row=0, column=13, padx=5, pady=5)

        self.TM_Add_Assembly_B.grid(row=1, column=13, padx=5, pady=5)

        self.TM_View_Request_B.grid(row=0, column=14, padx=5, pady=5)

        #----------------------------------------------------------------------------------------------------------------------------------------------
        #Frame 7 Sub Log/CSA
        self.Kit_Label_B.grid(row=0, column=0, padx=5, pady=5)

        self.frame7_Separator_Label_1.grid(row=1, column=0, columnspan=2)
        self.frame7_Separator_1.grid(row = 0, column = 1, sticky = "ns", rowspan = 3, padx = 5, pady = 5)
        #---------------------------------------------------------------------------------------------------------------------------------------------
        #Report Frame
        self.Report_Frame.grid(row = 1, column = 1, sticky = "w")
        #self.Report_Frame.config( highlightbackground="black", highlightthickness=1)
        self.Report_Text.grid(row = 0, column = 0)
        self.Report_Text.configure(yscrollcommand = self.Report_Scroll.set)
        
        self.Report_Scroll.grid(row = 0, column = 1, sticky = "ns")
        self.Clear_Report_B.grid(row = 1, column = 0, sticky = "w")
        #----------------------------------------------------------------------------------------------------------------------------------------------
        #Main Tree Frame
        self.Main_Tree_Frame.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = 5)
        
        self.Main_Tree.grid(row = 0, column = 0, sticky = "ew")
        
        self.Main_Tree.configure(yscrollcommand = self.Main_Tree_Scroll_Y.set, xscrollcommand = self.Main_Tree_Scroll_X.set)
        
        self.Main_Tree_Scroll_Y.grid(row = 0, column = 1, sticky = "ns")
        self.Main_Tree_Scroll_X.grid(row = 1, column = 0, sticky = "ew")
        self.Clear_Main_Tree_B.grid(row = 2, column = 0, sticky = "w", pady = (0,10))
        self.Export_Main_Tree_B.grid(row = 2, column = 0, sticky = "e", pady = (0,10))
        
        Main_Trees.Main_Tree_0(self.Main_Tree)
        
        self.Book.hide(1)
        self.Book.hide(2)
        self.Book.hide(3)
        self.Book.hide(4)
        self.Book.hide(5)
        self.Book.hide(6)
        self.Book.hide(7)

        return
    '''
    def PasswordCheck(self, root):

        6/10/22 SJ
        Add a password check to continue into interactive

        self.Password = simpledialog.askstring("Password", "Enter the Password", show='*')
        
        self.DEPT = "None"
        if self.Password == "METest":
            self.DEPT = 'ME'
        elif self.Password == "SubLogTest":
            self.DEPT = "SubLog"
        elif self.Password == "ProductionTest":
            self.DEPT = "Production"
        elif self.Password == None:
            root.destroy()
        else:
            messagebox.showerror("Password", "Incorrect Password, try again!")
            self.PasswordCheck(root)
    '''
    #Create a button function "Scan Part" in frame1
    def SN_To_Tote(self):
        while True:
            self.Book.update()
            SN = simpledialog.askstring("Serial Number", "Scan the Serial Number")
            self.Book.update()
            ID = simpledialog.askstring("Tote ID", "Scan the Tote ID")
        
            if SN == None:
                break
            elif ID == None:
                break
            else:   
                #Create Cursor
                c = self.conn.cursor()
                #Attempt to export SN & tote data to ManexExtras. (toteID = nvarchar(20) and sn = nvarchar(30))
                SP_AddSN = "EXEC ManexExtras.utec.W_SN_To_Tote @isn=?, @itote=?"
                AddSN_Params = (SN, ID)

                #Hopefully trap error if raised
                try:
                    c.execute(SP_AddSN, AddSN_Params)
                    c.commit()
                    #--------------------------------------------------------------
                    #5/16/2022 NS - This bit of code was stolen from Q_Tote_Summary to show the current tote quantity after a SN has been scanned into the system. 
                    c01 = []
                    c01.append(ID)
                    if c01 == []:
                        return
                    c = self.conn.cursor()
                    l = len(c01)
                    self.param_array=[]     
                    for i in range(l):
                        self.param_array.append([c01[i]]) 
                    TOTE_DISPLAY="EXEC ManexExtras.utec.Q_Tote_Summary @toteIDs=?"
                    c.execute(TOTE_DISPLAY,[self.param_array])
                    data = c.fetchall() 
                    print(data)  
                    row_count = 0      
                    for row in data :
                        Qty = row[4]
                    print("Quantity=",Qty)
                    #---------------------------------------------------------------
                    self.Report_Text.configure(state = NORMAL)
                    self.Report_Text.insert(END, SN + " has been added to Tote " + ID + " ("+ str(Qty) + "/48)\n")
                    self.Report_Text.configure(state = DISABLED)
                    self.Report_Text.see("end")
                    
                except Exception as e:
                    self.e1 = str(e)
                    self.Report_Text.configure(state = NORMAL)
                    self.Report_Text.insert(END, self.e1 + "\n")
                    self.Report_Text.configure(state = DISABLED)
                    self.Report_Text.see("end")
           
                c.commit()
                #close/delete cursor (no need to commit for SQL Server)
                c.close()
                Main_Trees.Clear_Main_Tree(self.Main_Tree)
                self.WO_SN_Count_V.set(0)
                self.WO_SN_V.set(0)      
        return

    #Create a button function New Tote ID in frame1
    def New_Tote_ID(self):
        
        WO = self.WONO_V.get()
        Count = self.Tote_Cap.get()
        Count_Int = int(Count)

        while Count_Int < 48:
        
            New_Tote_ID_Result = messagebox.askquestion("Bypass?", "The most current tote is not full, do you want to continue?", icon='warning')
            if New_Tote_ID_Result == 'yes':
                break
            else:
                return

        #Create Cursor
        c = self.conn.cursor()
        
        #Attempt to export SN & tote data to ManexExtras. (toteID = nvarchar(20) and sn = nvarchar(30))
        SP_NewTote = "EXEC ManexExtras.utec.W_New_Tote_ID @iwo=?"
    
        #Hopefully trap error if raised
        try:
            c.execute(SP_NewTote, WO)

            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, "New Tote ID has been Created \n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        except Exception as e:
            #messagebox.showwarning("Error",e)
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        c.commit()
        #close/delete cursor (no need to commit for SQL Server)   
        c.close()
        
        self.WO_Tote()

        return
    
    #Print Tote ID button frame1
    def Utec_Label_Print(self):
        os.startfile('S:\\_ENG_MANUFACTURING\\Applications\\Inter-Active\\REV_5\\Bar_Code-Active REV 2.lbx','print')
        return
       
    #Create a button function "Add Totes" frame1 and frame3
    def Tote_SN(self):
        
        '''
        6/7/22 SJ
        Rearranged main_tree_1 to be next to clear main tree, and the variables to be next to each other
        '''
        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        Main_Trees.Main_Tree_1(self.Main_Tree)

        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)
        self.Tote_Label_Count_V.set(0)
        self.SN_Label_Count_V.set(0)
        
        c01 = []
        
        while True:
            self.Book.update()
            ID = simpledialog.askstring("Tote ID", "Scan the Tote ID")
            if ID == None:
                break
            elif ID in c01:
                #messagebox.showwarning("Wrong Tote",ID + " has already been scanned, scan a different Tote ID")
                self.Report_Text.configure(state = NORMAL)
                self.Report_Text.insert(END,ID + " has already been scanned, scan a different Tote ID\n")
                self.Report_Text.configure(state = DISABLED)
                self.Report_Text.see("end")
            else:
                c01.append(ID)
        
        if c01 == []:
            return
    
        c = self.conn.cursor()
        l = len(c01)
        self.param_array=[]     
        for i in range(l):
            self.param_array.append([c01[i]]) 

        TOTE_DISPLAY="EXEC ManexExtras.utec.Q_Tote_SN @toteIDs=?"
        c.execute(TOTE_DISPLAY,[self.param_array])
    
        data = c.fetchall()
        print(data)
    
        row_count = 0      
        for row in data :
            row_count = row_count + 1
            self.Main_Tree.insert(parent ='', index= 'end', iid=row_count, text="", values=(row[3],row[1],row[2],row[4]))
         
        c.commit() 
        #Close Connection
        c.close()

        self.queue_list = data
        npdata = np.array(data)
    
        if data == []:
            #messagebox.showwarning("No SNs", "There are no SN's assigned to this Tote")
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END,"There are no SN's assigned to this Tote\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            return
        
        tote_count = len(np.unique(npdata[:,1]))
        
        self.Tote_Label_Count_V.set(tote_count)
        self.SN_Label_Count_V.set(row_count)
        
        return
    
    #Tote Summary button frame2
    def Q_Tote_Summary(self):
        
        '''
        6/7/22 SJ
        Rearranged Main_Tree_5 to be next to Clear_Main_Tree
        '''
        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        Main_Trees.Main_Tree_5(self.Main_Tree)

        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)

        c01 = []
        
        while True:
            self.Book.update()
            ID = simpledialog.askstring("Tote ID", "Scan the Tote ID")
            if ID == None:
                break
            elif ID in c01:
                #messagebox.showwarning("Wrong Tote",ID + " has already been scanned, scan a different Tote ID")
                self.Report_Text.configure(state = NORMAL)
                self.Report_Text.insert(END,ID + " has already been scanned, scan a different Tote ID\n")
                self.Report_Text.configure(state = DISABLED)
                self.Report_Text.see("end")
            else:
                c01.append(ID)
        
        if c01 == []:
            return
    
        c = self.conn.cursor()
        l = len(c01)
        self.param_array=[]     
        for i in range(l):
            self.param_array.append([c01[i]]) 
            
        TOTE_DISPLAY="EXEC ManexExtras.utec.Q_Tote_Summary @toteIDs=?"
        
        #Trap error if raised
        try:
            c.execute(TOTE_DISPLAY,[self.param_array])
            data = c.fetchall()
            
            row_count = 0      
            for row in data :
                row_count = row_count + 1
                self.Main_Tree.insert(parent ='', index= 'end', iid=row_count, text="", values=(row[0],row[1],row[2],row[3],row[4]))
                print(data)
    
            print(data)

        except Exception as e:
            #messagebox.showinfo("Results",e)
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
                 
        c.commit()
        c.close()
        
        return
    
    #View Last SN button frame2
    def View_Last_SN(self):
    
        c = self.conn.cursor()
            
        PARAM = "SELECT TOP (1) [SERIALNO] FROM [ManexExtras].[utec].[SERIAL] ORDER BY SERIALNO desc"
        
        #Trap error if raised
        try:
            c.execute(PARAM)
            output = np.array(c.fetchall())
            output1 = output[0,0]
            
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, output1 + " is the most recent Serial Number created\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        except Exception as e:
            #messagebox.showinfo("Results",e)
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
                 
        c.commit()
        c.close()
        
        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)
    
        return
    
    #Delete SN button frame1
    def Remove_SN_From_Tote(self):

        self.Book.update()

        SN = simpledialog.askstring("Serial Number", "Scan the Serial Number")
        WO = self.WONO_V.get()
    
        c = self.conn.cursor()
            
        TOTE_DISPLAY= "EXEC ManexExtras.utec.W_Remove_SN_From_Tote @isn=?, @iwo=?"
        
        #Trap error if raised
        try:
            c.execute(TOTE_DISPLAY,SN,WO)
            output1 = c.fetchall()
            print(output1)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, "Serial Number: " + SN + " has been removed from the tote. \n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        except Exception as e:
            #messagebox.showinfo("Results",e)
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
                 
        c.commit()
        c.close()
        
        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)
    
        return

    #Delete Tote ID button frame1            
    def Delete_Tote(self):

        self.Book.update()
        ID = simpledialog.askstring("Tote ID", "Scan the Tote ID")
    
        c = self.conn.cursor()
            
        TOTE_DISPLAY="EXEC ManexExtras.utec.W_Delete_Tote @itote=?"
        
        #Trap error if raised
        try:
            c.execute(TOTE_DISPLAY,ID)
            
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, "Tote " + ID + " has been deleted \n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")

        except Exception as e:
            #messagebox.showinfo("Results",e)
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
 
        c.commit()
        c.close()
        
        self.WO_Tote()
    
        return
 
    #PL Report button frame3
    def Q_PL_Report(self):

        self.Book.update()
        ipl = simpledialog.askstring("Packlist", "Enter The Packlist Number")
        if ipl == "":
            return
           
        c = self.conn.cursor()
        
        PACK= "EXEC ManexExtras.utec.Q_PL_Report @ipl=?"

        try:
            c.execute(PACK,ipl)
            data_3 = c.fetchall()
            
        except Exception as e:
            self.e1 = str(e)    
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        c.commit()
        c.close()

        self.Book.update()              
        self.Todays_Date = simpledialog.askstring("Todays Date", "Enter Todays Date")
        if self.Todays_Date == None:
            return
        else:
            self.f = open("S:\\_ENG_MANUFACTURING\\Applications\\Inter-Active\\Exported Data\\" + self.Todays_Date + ".csv","x", newline="")
            self.writer = csv.writer(self.f)
            
            self.header = ("Date","ProActive Box ID","AAI P/N","Customer P/N","Software rev","ProActive S/N","Manufacture","Purchase Order","Mac Address")
            self.writer.writerow(self.header)
            
            for self.record in data_3:
                self.record[2] = self.record[2] + 'P'
                self.writer.writerow(self.record)
            self.f.close()
            
        return
       
    #Create an Export Packlist Button frame3
    def Add_Pl_Get_Cust_View(self):
        
        data_1 = self.param_array

        self.Book.update()
        ipl = simpledialog.askstring("Packlist", "Enter The Packlist Number")
        if ipl == "":
            return
  
        c = self.conn.cursor()
        
        PACK= "EXEC ManexExtras.utec.W_Add_Pl_Get_Cust_View @ipl=?, @toteIDs=?"

        try:
            c.execute(PACK,ipl,data_1)
            data_2 = c.fetchall()
            
        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        c.commit()
        c.close()

        self.Book.update()
        self.Todays_Date = simpledialog.askstring("Todays Date", "Enter Todays Date")
        if self.Todays_Date == None:
            return
        else:
            self.f = open("S:\\_ENG_MANUFACTURING\\Applications\\Inter-Active\\Exported Data\\" + self.Todays_Date + ".csv","x", newline="")
            self.writer = csv.writer(self.f)
            
            self.header = ("Date","ProActive Box ID","AAI P/N","Customer P/N","Software rev","ProActive S/N","Manufacture","Purchase Order","Mac Address")
            self.writer.writerow(self.header)
            
            for self.record in data_2:
                self.writer.writerow(self.record)
            self.f.close()
            
        return

 
    #Import SN's button frame2
    def Import_SN(self):

        self.Book.update()
        self.firstSN = simpledialog.askstring("First SN","Enter the first Serial Number")
        self.Book.update()
        self.Qty = simpledialog.askstring("SN Quantity","Enter the Quantity of desired SN's")
        
        self.WO = self.WO_SN_V.get()
        self.c = self.conn.cursor()
        
        self.input2 = "EXEC ManexExtras.utec.W_Import_SN @firstSN=?, @snQty=?, @iwo=?"
        
        #Trap error if raised
        try:
            self.c.execute(self.input2, self.firstSN, self.Qty, self.WO)
        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
        
        self.c.commit()
        self.c.close() 
        
        return
    #Clear button in Report Frame     
    def Clear_Report(self):
        self.Report_Text.configure(state = NORMAL)
        self.Report_Text.delete('1.0',END)
        self.Report_Text.configure(state = DISABLED)
        self.Report_Text.see("end")
        return
    
    #Add WO# button frame1
    def WO_Tote(self):

        self.Book.update()
        WO = simpledialog.askstring("WO#", "Enter the Work Order Number")
      
        if WO == "":
            return
        elif WO == None:
            return
        else:
        
            self.WONO_V.set(WO)
              
            TOTE_DISPLAY="EXEC ManexExtras.utec.Q_WO_Tote @iwo=?, @showShipped=?"
            
            #Trap error if raised
            try:
                c = self.conn.cursor()
                
                shipped = messagebox.askquestion("Show Shipped?", "Do you want to show the Totes that have already been shipped?", icon='info')
                if shipped == 'yes':
                    WO_Tote_Result = 1
                else:
                    WO_Tote_Result = 0
                
                c.execute(TOTE_DISPLAY, WO, WO_Tote_Result)
                
                self.Test_Result = c.fetchall()
                
                c.commit()
                c.close()
                
                self.Tote_Display = np.array(self.Test_Result)            
    
                try:          
                    self.Tote_List_1 = list(self.Tote_Display[:,0])
                                            
                except Exception:
                    self.Report_Text.configure(state = NORMAL)
                    self.Report_Text.insert(END, "Error, There are no totes assigned to this Work Order \n")
                    self.Report_Text.configure(state = DISABLED)
                    self.Report_Text.see("end")
                
                Drop_List = []
                
                count_end = len(self.Tote_Display[:,0])
            
                count = 0
                while count is not count_end:
                    
                    tote = str(self.Tote_Display[count,0])
                    quant = str(self.Tote_Display[count,3])
                    
                    Drop_List.append(tote + " " + quant + "/48")
                    
                    count = count + 1

                #self.Tote_Drop_V.set(self.Tote_List_1[0])
                self.Tote_Drop_V.set(Drop_List[0])
                
                menu = self.Tote_Drop["menu"]
                menu.delete(0, "end")
                
                #for string in self.Tote_List_1:
                for string in Drop_List:
                    menu.add_command(label=string,command=lambda value=string: self.Tote_Drop_V.set(value))
    
            except Exception as e:
                #messagebox.showinfo("Results",e)
                self.e1 = str(e)
                self.Report_Text.configure(state = NORMAL)
                self.Report_Text.insert(END, self.e1 + "\n")
                self.Report_Text.configure(state = DISABLED)
                self.Report_Text.see("end")
        
                self.Tote_List = ['P#######']
                self.Tote_Drop_V.set(self.Tote_List[0])
                menu = self.Tote_Drop["menu"]
                menu.delete(0, "end")

            return 
    
    #Add WO# button frame2
    def WO_SN(self):
        
        '''
        6/7/22 SJ
        Main_Tree_2 rearranged to be next to Clear_Main_Tree
        '''
        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        Main_Trees.Main_Tree_2(self.Main_Tree)

        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)
              
        c = self.conn.cursor()
            
        TOTE_DISPLAY="EXEC ManexExtras.utec.Q_WO_SN @iwo=?, @filter=?"
        
        #Trap error if raised
        try:
            result = self.WO_Options_V.get()
            if result == "Select All":
                option_1 = 0
            elif result == "Select Assigned":
                option_1 = 1
            elif result == "Select Unassigned":
                option_1 = 2
            else:
                option_1 = 3
                
            self.Book.update()
            WO = simpledialog.askstring("WO#", "Enter the Work Order Number")
            self.WO_SN_V.set(WO)
            #WO = self.WONO_V.get()
            
            c.execute(TOTE_DISPLAY,WO,option_1)
            data = c.fetchall()
            print(data)
    
            row_count = 0      
            for row in data :
                row_count = row_count + 1
                self.Main_Tree.insert(parent ='', index= 'end', iid=row_count, text="", values=(row[2],row[0],row[1]))

            self.WO_SN_Count_V.set(row_count)

        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        c.commit()
        c.close()     
        
        return
    
    def Update_Tote_Label(self):
        c = self.conn.cursor()
            
        W_Update_Tote_Label_1 ="EXEC ManexExtras.utec.W_Update_Tote_Label @itote=?"
        ID = self.Tote_Drop_V.get()
        
        if len(ID) == 15:
            ID1 = ID[:-6]
        else:
            ID1 = ID[:-5]
        
        #Trap error if raised
        try:                      
            c.execute(W_Update_Tote_Label_1,ID1)
        
        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
    
        c.commit()
        c.close()
        return
    
    def callback(self,*args):
        result = self.Tote_Drop_V.get()
        if result == 'P#######':
            return
        else:
            self.Update_Tote_Label()
            self.Tote_Capacity()
        return
    
    def Tote_Capacity(self):
        c = self.conn.cursor()
            
        Tote_Capacity_1 ="EXEC ManexExtras.utec.Q_Tote_Capacity @iwo=?"
        
        #ID = self.Tote_Drop_V.get()
        WO = self.WONO_V.get()
        
        #Trap error if raised
        try:                      
            c.execute(Tote_Capacity_1,WO)
            count = c.fetchall()
            np_count = np.array(count)

            #Tote_Number = str(list(np_count[:,0])).replace("'","")[1:-1]

            Serial_Count = str(list(np_count[:,1])).replace("'","")[1:-1]
            
            # self.Report_Text.configure(state = NORMAL)
            # self.Report_Text.insert(END, Tote_Number + " has " + Serial_Count + " SN's \n")
            # self.Report_Text.configure(state = DISABLED)
            # self.Report_Text.see("end")
            
            self.Tote_Cap.set(str(Serial_Count))

        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        c.commit()
        c.close()
        return
    
    def callback2(self,*args):
        self.WO_SN()
        return
    
    def Delete_All_SNs_From_WO(self):
        c = self.conn.cursor()
            
        Delete_All_SNs ="EXEC ManexExtras.utec.W_Delete_All_SNs_From_WO @iwo=?"
        
        WO = self.WO_SN_V.get()
        
        #Trap error if raised
        try:                      
            c.execute(Delete_All_SNs,WO)
            
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, "All SN's from WO#" + WO + " have been deleted \n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        c.commit()
        c.close()
        
        return
    
    def SN_Info(self):
        
        '''
        6/7/22 SJ
        Rearranged Main_Tree_3 to be next to Clear_Main_Tree
        '''
        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        Main_Trees.Main_Tree_3(self.Main_Tree)

        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)
        c = self.conn.cursor()
            
        SN_DISPLAY="EXEC ManexExtras.utec.Q_SN_Info @isn=?"
        
        #Trap error if raised
        try:        
            self.Book.update()
            SN = simpledialog.askstring("SN", "Enter the Serial Number")
                
            c.execute(SN_DISPLAY,SN)
            data = c.fetchall()
            print(data)
        
            row_count = 0      
            for row in data :
                row_count = row_count + 1
                self.Main_Tree.insert(parent ='', index= 'end', iid=row_count, text="", values=(row[0],row[1],row[2],row[3],row[4]))
            
        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
            
        c.commit()
        c.close()

        return
    
    def Ultratec(self, root):

        '''
        6/7/22 SJ
        Check the department of the logged in user to see if have permission to view this Program -- See Get_User_Dept()
        
        6/10/22 SJ
        commenting this out due to an error

        if self.DEPT != "ME" and self.DEPT != "Operations" and self.DEPT != "Quality" and self.DEPT != "Production":
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, "You Do Not Have Access to This Program" + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")

        else:
        '''

        '''    
        6/7/22 SJ
        Update title to show which program in Interactive you have selected.
        '''
        root.title('Inter-Active 1.8.2/Ultratec')

        self.Book.hide(4)
        self.Book.hide(5) 
        self.Book.hide(6)
        self.Book.hide(7)
        self.Book.add(self.frame1, text=" Production ")
        '''
        6/9/22 SJ
        Selects the first tab of Ultratec when the button is pressed
        '''
        self.Book.select(1)
        #Only show the ME tab of ultratec to ME, Operations, and Quality - commented out due to errors
        #if self.DEPT == "ME" or self.DEPT == "Operations" or self.DEPT == "Quality":
        self.Book.add(self.frame2, text = " ME ")
        self.Book.add(self.frame3, text = " Materials ")
        '''
        6/7/22 SJ
        Rearranged Main_Tree_0 to be next to Clear_Main_Tree
        '''
        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        Main_Trees.Main_Tree_0(self.Main_Tree)

        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)
            
        return
    
    def Label_Printing(self, root):
        '''
        6/7/22 SJ
        Limit who can access this Program based on the department of the logged in User -- See Get_User_Dept()
        
        6/10/22 SJ
        commenting this out due to errors

        if self.DEPT != "ME" and self.DEPT != "Operations" and self.DEPT != "Quality" and self.DEPT != "Production":
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, "You Do Not Have Access to This Program" + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
        else:
        '''

        '''
        6/7/22 SJ
        Update title to show which program in Interactive you have selected.
        '''
        root.title('Inter-Active 1.8.2/Materials')

        self.Book.hide(1)
        self.Book.hide(2)
        self.Book.hide(3)
        self.Book.hide(5)
        self.Book.hide(6)
        #6/15/22 SJ changed from Materials to Label Printing
        self.Book.add(self.frame4, text=" Label Printing ")
        self.Book.add(self.frame7, text=" Kitting ")
        '''
        6/9/22 SJ
        Automatically select the Materials tab when Label Printing button is pressed
        '''
        self.Book.select(4)
        
        '''
        6/7/22 SJ
        Rearranged Main_Tree_0 to be next to Clear_Main_Tree
        '''
        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        Main_Trees.Main_Tree_0(self.Main_Tree)

        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)
            
        return
    
    def Sub_Log(self, root):

        self.Main_Tree.bind('<ButtonRelease-1>', partial(Sub_Log_Files.selectItem,self.Main_Tree,self.Sub_Request_V))
        '''
        6/7/22 SJ
        Limit who can access this Program based on the department of the logged in User -- See Get_User_Dept()

        6/10/22 SJ
        commenting this out due to errors
        
        if self.DEPT != "ME" and self.DEPT != "Operations" and self.DEPT != "Quality" and self.DEPT != "Supply Chain" and self.DEPT != "Customer Service":
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, "You Do Not Have Access to This Program" + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
        else:
        '''

        '''
        6/7/22 SJ
        Update title to show which program in Interactive you have selected.
        '''
        root.title('Inter-Active 1.8.2/Sub_Log')

        self.Book.hide(1)
        self.Book.hide(2)
        self.Book.hide(3)
        self.Book.hide(4)
        self.Book.hide(6)
        self.Book.hide(7)
        self.Book.add(self.frame5, text=" Supply Chain ")
        #self.Book.add(self.frame6, text=" ME ")
        #self.Book.add(self.frame7, text=" CAS ")
        '''
        6/9/22 SJ
        Automatically select the Supply Chain tab when Sub Log button is pressed
        '''
        self.Book.select(5)
        
        '''
        6/7/22 SJ
        Moved Clear_Main_Tree to be after the variables
        '''
        self.WO_SN_Count_V.set(0)
        self.WO_SN_V.set(0)
        self.Sub_Request_V.set(None)

        Main_Trees.Clear_Main_Tree(self.Main_Tree)
        Sub_Log_Files.sub_request_populate(self.Main_Tree,self.Sub_Options_V,self.Report_Text,self.Sub_clicked)
    
        return         
    #populates sub requests whenever a Sub_Options_V is selected
    def callback3(self,*args):
        Sub_Log_Files.sub_request_populate(self.Main_Tree,self.Sub_Options_V,self.Report_Text,self.Sub_clicked)
        '''
        6/7/22 SJ
        Set Sub_Request_V to None instead of 0, as it is set to None when Interactive is opened.
        Also used for functions that check if a sub request has been selected.
        '''
        self.Sub_Request_V.set(None)
        return
    #populates sub requests whenever a Responsible Party is selected
    def callback4(self,*args):
        Sub_Log_Files.sub_request_populate_resp(self.Main_Tree,self.Sub_clicked,self.Report_Text,self.Sub_Options_V)
        self.Sub_Request_V.set(None)
        return
    #populate task manager based on responsible party
    def callback5(self,*args):
        Task_Manager.TM_populate_status(self.Main_Tree,self.TM_Options_V,self.Report_Text,self.ME_clicked)
        self.Sub_Request_V.set(None)
        return
        
    def W_SN_To_Scrap(self):
        conn1 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=ManexExtras;"
                               "Trusted_Connection=yes;")
        c = conn1.cursor() 
        WO = self.WO_SN_V.get()
        self.Book.update()
        SN = simpledialog.askstring("Serial Number", "Enter the Serial Number")
        EXE_STRING = "EXEC ManexExtras.utec.W_SN_To_Scrap @isn=?, @iwo=?"
        try:    
            c.execute(EXE_STRING,SN,WO)
        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
                 
        c.commit()
        c.close()
        return

    def Q_Check_For_Issues(self):
        conn1 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=ManexExtras;"
                               "Trusted_Connection=yes;")
        c = conn1.cursor() 
        EXE_STRING = "EXEC ManexExtras.utec.Q_Check_For_Issues"
        try:    
            c.execute(EXE_STRING) 
            data = c.fetchall()
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, str(data) + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
                   
        except Exception as e:
            self.e1 = str(e)
            self.Report_Text.configure(state = NORMAL)
            self.Report_Text.insert(END, self.e1 + "\n")
            self.Report_Text.configure(state = DISABLED)
            self.Report_Text.see("end")
                 
        c.commit()
        c.close()
        return 

def main():
    root = Tk()    
    InterActive(root)
    root.mainloop()
   
if __name__ == '__main__':
    main()
