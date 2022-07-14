import pyodbc
import numpy as np
import os
def TM_Get_Names():
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    '''
    6/7/22 SJ
    Connect to the Interactive to pull the list of users in ME for the Task Manager and create a dropdown list.
    '''
    TM_EXE_STRING = "EXEC Interactive.dbo.Populate_ME"
    c.execute(TM_EXE_STRING)
    ME_data = c.fetchall()
    ME_USERS = np.array(ME_data)
    ME_names = ["All", "ME"]
    ME_rowcount = 0

    #format names from manex to look better
    for row in ME_USERS:
        ME_names.append(ME_USERS[ME_rowcount,0].strip() + " " + ME_USERS[ME_rowcount,1].strip())
        ME_rowcount += 1

    return ME_names