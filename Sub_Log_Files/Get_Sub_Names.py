import pyodbc
import numpy as np
import os

def Get_Sub_Names():
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                               "Server=DC01;"
                               "Database=Interactive;"
                               "Trusted_Connection=yes;")
    c = conn2.cursor()
    '''
    6/7/22 SJ
    Connect to database to fetch a list of Users for the Sub Log to sort by.
    '''
    Sub_EXE_STRING = "EXEC Interactive.dbo.SUB_Populate_Users"
    c.execute(Sub_EXE_STRING)
    Sub_data = c.fetchall()
    Sub_USERS = np.array(Sub_data)
    Sub_names = ["All", "Supply Chain", "ME", "CAS"]
    Sub_rowcount = 0

    for row in Sub_USERS:
        Sub_names.append(Sub_USERS[Sub_rowcount,0].strip() + " " + Sub_USERS[Sub_rowcount,1].strip())
        Sub_rowcount += 1

    return Sub_names