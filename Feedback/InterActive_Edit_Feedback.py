import pyodbc
import numpy as np
from tkinter import Toplevel
from tkinter import Label
from tkinter import Text
from tkinter import WORD
from tkinter import END
from tkinter import Button
from tkinter import DISABLED
from tkinter import NORMAL 
from tkinter import simpledialog
'''
6/9/22 SJ
Code coppied mostly from Interactive_Submit_Feedback
asks for a password and then will allow the user to edit the current feedback if they enter the password correctly
'''
def Edit_Feedback(Report_Text):

	conn2 = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server=DC01;"
                           "Database=Interactive;"
                           "Trusted_Connection=yes;")
	c = conn2.cursor()

	Password = simpledialog.askstring("Password", "Enter the Password", show='*')

	if Password == "AdminTest":

		EXE_STRING = "EXEC Interactive.dbo.View_Feedback"

		try:
			c.execute(EXE_STRING)
			data = c.fetchall()
			np_data = np.array(data)
			note = str(np_data[0])

			if note == '[None]':
			    note = note[1:-1]
			else:
			    note = note[2:-2]
			note = note.replace(r'\n','\n')
			note = note.replace(r'\t','\t')

			top = Toplevel()
			top.geometry("600x250")
			top.title('Feedback Editting')

			name = Label(top,text = "Enter Your Feedback or Suggestions")
			name.pack()

			e1 = Text(top, width = 60, height = 10, wrap = WORD)
			e1.pack()
			e1.insert(END,note)

			btn = Button(top, text = "Submit", command = lambda: sub_submit(e1.get("1.0",'end-1c')))
			btn.pack()  
		except Exception as e:
			e1 = str(e)
			Report_Text.configure(state = NORMAL)
			Report_Text.insert(END, e1 + "\n")
			Report_Text.configure(state = DISABLED)
			Report_Text.see("end")        
	    

		def sub_submit(e1):

			NOTE = e1
	       
			try:
				EXE_STRING = "EXEC Interactive.dbo.Submit_Feedback @note=?"
				c.execute(EXE_STRING,NOTE)  
			except Exception as e:
				e1 = str(e)
				Report_Text.configure(state = NORMAL)
				Report_Text.insert(END, e1)
				Report_Text.configure(state = DISABLED)
				Report_Text.see("end")        
			c.commit()
			c.close()
			top.destroy()
			top.update()

			return
	elif Password == None:
		pass

	else:
		Report_Text.configure(state = NORMAL)
		Report_Text.insert(END, "Wrong Password\n")
		Report_Text.configure(state = DISABLED)
		Report_Text.see("end")
	return