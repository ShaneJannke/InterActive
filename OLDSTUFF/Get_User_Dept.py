import pyodbc
import numpy as np
import os
import getpass
#gets the Department of the user from Manex based on their login
def Get_User_Dept():
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=Testdatabase;"
                               "Trusted_Connection=yes;")
        
    c = conn2.cursor()

    #get login of user
    #USERNAME = os.getlogin()
    USERNAME = getpass.getuser()
    #seperate first name from last name
    name = USERNAME.split(".")
    fname = name[0].capitalize()
    lname = name[1].capitalize()
    #get department from manex for given first and last name
    EXE_STRING = "EXEC Testdatabase.dbo.Get_User_Dept @fname=?, @lname=?"
    c.execute(EXE_STRING,fname,lname)
    data = c.fetchall()
    userdept = np.array(data)
    dept = []

    rowcount = 0
    for row in userdept:
        dept.append(userdept[rowcount,0])
        rowcount += 1
    c.close()

    #remove white space from department name
    deptcheck = dept[0].strip()
    #Return Department Name to Interactive, used to limit programs
    if deptcheck == "MFG ENGINEERING":
        return "ME"
    if deptcheck == "OPERATIONS":
        return "Operations"
    if deptcheck == "QUALITY":
        return "Quality"                
    elif deptcheck == "PRODUCTION":
        return "Production"
    elif deptcheck == "PURCHASING":
        return "Supply Chain"
    elif deptcheck == "CUST SERVICE":
        return "Customer Service" 