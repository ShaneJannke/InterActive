import pyodbc
import numpy as np
import os
def Get_TM_Names():
    conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Testdatabase;"
                           "Trusted_Connection=yes;")
    c = conn2.cursor()
    '''
    6/7/22 SJ
    Connect to the testdatabase to pull the list of users in ME for the Task Manager and create a dropdown list.
    '''
    TM_EXE_STRING = "EXEC Testdatabase.dbo.Populate_ME"
    c.execute(TM_EXE_STRING)
    ME_data = c.fetchall()
    ME_USERS = np.array(ME_data)
    ME_names = ["All", "ME"]
    ME_rowcount = 0

    for row in ME_USERS:
        ME_names.append(ME_USERS[ME_rowcount,0].strip() + " " + ME_USERS[ME_rowcount,1].strip())
        ME_rowcount += 1

    return ME_names