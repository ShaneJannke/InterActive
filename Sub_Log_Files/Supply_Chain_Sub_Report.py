import pyodbc
import numpy as np
from tkinter import NORMAL
from tkinter import END
from tkinter import DISABLED

def Supply_Chain_Sub_Report(Sub_Request_V,Report_Text):
    
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    ID = Sub_Request_V.get()   
    
    exe_String = "EXEC Interactive.dbo.SUB_By_ID @ID=?"
    
    try:
        data = c.execute(exe_String,ID) #Ordering by WONO because to avoid errors from the same Work Order being added at different times.
        data = c.fetchall()
        np_data = np.array(data)

        Unique_Key_List = [] #Creating a Unique List of component requests to identify blocks of specific component requests
        Unique_Key_Row_List = []
        Unique_PCBA_List = [] #This identifies unique pcba's
        Unique_CUST_PCBA_List = [] #identies unique customer pcba's 
        row_count = 0
        for row in np_data:
            if str(np_data[row_count,5])+str(np_data[row_count,13])+str(np_data[row_count,11]) not in Unique_Key_List:
                Unique_Key_List.append(str(np_data[row_count,5])+str(np_data[row_count,13])+str(np_data[row_count,11]))
                Unique_Key_Row_List.append(row_count)
            if str(np_data[row_count,13])+" REV "+ str(np_data[row_count,14]) not in Unique_PCBA_List:
                Unique_PCBA_List.append(str(np_data[row_count,13])+" REV "+ str(np_data[row_count,14]))
            if str(np_data[row_count,16])+" REV "+str(np_data[row_count,17]) not in Unique_CUST_PCBA_List:
                Unique_CUST_PCBA_List.append(str(np_data[row_count,16])+" REV "+str(np_data[row_count,17]))
            row_count = row_count + 1
        
        def convert_(i,j): #This funciton removes '' from the outside of our strings 
            k = np_data[i,j]
            k = str(k)
            k = k.strip()  
            return k
        
        #Algorithm meant to convert our np_data into the Alternate_Report
        Alternate_Report = ""
        row_count = 0
        for row in Unique_Key_List:
            Ref_Des = []
            row_count_2 = 0
            row_count_3 = Unique_Key_Row_List[row_count]
            for row in np_data:
                Key = str(Unique_Key_List[row_count])
                Key = Key.strip()
                if Key == (str(np_data[row_count_2,5])+str(np_data[row_count_2,13])+str(np_data[row_count_2,11])):
                    Ref_Des.append(convert_(row_count_2,19))
                row_count_2 = row_count_2 + 1
            Next_String =  ("Component:\n"+str(np_data[row_count_3,7])+" | "+str(np_data[row_count_3,6])+" ("+str(np_data[row_count_3,5])+")\n\n"+
                            "PCBA:\n"+convert_(row_count_3,12)+" ("+convert_(row_count_3,13)+" REV "+convert_(row_count_3,14)+" | "+convert_(row_count_3,16)+" REV "+convert_(row_count_3,17)+")\n\n"+
                            "Reference Designator(s):\n"+str(','.join(Ref_Des))+"\n\n"+
                            "Sales Order:\n"+convert_(row_count_3,10)+"\n\n"+
                            "Work Order:\n"+convert_(row_count_3,11)+"\n\n"+
                            "Quantity Needed:\n"+convert_(row_count_3,18)+"\n\n"+
                            "We were wondering if we could use this alternate:"+"\n"+
                            "Substitute Component:\t***Place the Mfgr & Mfgr PN here***\n"+
                            "***Put a screen shot of the component comparison here***\n\n")
            Alternate_Report = Alternate_Report + Next_String
            row_count = row_count + 1
        
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, 
                                "HEADER \n" +
                                "Component Substitution Request #"+convert_(0,0)+" | "+convert_(0,15)+" | "+str(','.join(Unique_PCBA_List))+" | "+str(','.join(Unique_CUST_PCBA_List))+" | \n\n"+
                                "BODY \n" +
                                "Component Substitution Request #"+convert_(0,0)+" has been generated to address the following component shortage(s): \n\n"+
                                "There is not enough available stock of:\n"+
                                "---------------------------------------------------------------------------\n\n"+
                                Alternate_Report+
                                "---------------------------------------------------------------------------\n\n\n\n")
                                
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")  
    except Exception as e:
        e1 = str(e)
        Report_Text.configure(state = NORMAL)
        Report_Text.delete('1.0',END)
        Report_Text.insert(END, e1 + "\n")
        Report_Text.configure(state = DISABLED)
        Report_Text.see("1.0")       
    c.commit()
    c.close() 
    return