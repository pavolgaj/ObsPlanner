import sys

from tkinter import *
from tkinter import messagebox  
import tkinter.ttk as ttk

def save():
    global top
    note=Text1.get("1.0",END)
    print()
    top.destroy()
    
def detect():
    constVar.set('aaa')

top = Tk()
top.geometry("370x450")
top.title("Object")

nameVar=StringVar(top)
raVar=StringVar(top)
decVar=StringVar(top)
constVar=StringVar(top)
magVar=DoubleVar(top)
sizeVar=StringVar(top)
typeVar=StringVar(top)

#objekty
Label1 = Label(top)
Label1.place(relx=0.08, rely=0.07, height=21, width=43)
Label1.configure(text='''Name''')

Entry1 = Entry(top)
Entry1.place(relx=0.3, rely=0.07,height=23, relwidth=0.45)
Entry1.configure(background="white")
Entry1.configure(textvariable=nameVar)

Label2 = Label(top)
Label2.place(relx=0.14, rely=0.16, height=21, width=22)
Label2.configure(text='''RA''')

Entry2 = Entry(top)
Entry2.place(relx=0.38, rely=0.18,height=23, relwidth=0.45)
Entry2.configure(background="white")
Entry2.configure(textvariable=raVar)

Label3 = Label(top)
Label3.place(relx=0.11, rely=0.24, height=21, width=31)
Label3.configure(text='''DEC''')

Entry3 = Entry(top)
Entry3.place(relx=0.35, rely=0.24,height=23, relwidth=0.45)
Entry3.configure(background="white")
Entry3.configure(textvariable=decVar)

Label8 = Label(top)
Label8.place(relx=0.08, rely=0.33, height=21, width=90)
Label8.configure(text='''Constellation''')

Entry7 = Entry(top)
Entry7.place(relx=0.38, rely=0.33,height=23, relwidth=0.29)
Entry7.configure(background="white")
Entry7.configure(textvariable=constVar)

Button2 = Button(top)
Button2.place(relx=0.73, rely=0.33, height=29, width=69)
Button2.configure(text='''Detect''')
Button2.configure(command=detect)  

Label4 = Label(top)
Label4.place(relx=0.11, rely=0.4, height=21, width=32)
Label4.configure(text='''Mag''')

Entry4 = Entry(top)
Entry4.place(relx=0.35, rely=0.42,height=23, relwidth=0.45)
Entry4.configure(background="white") 
Entry4.configure(textvariable=magVar)

Label5 = Label(top)
Label5.place(relx=0.11, rely=0.53, height=21, width=31)
Label5.configure(text='''Size''')

Entry5 = Entry(top)
Entry5.place(relx=0.3, rely=0.53,height=23, relwidth=0.45)
Entry5.configure(background="white") 
Entry5.configure(textvariable=sizeVar) 

Label6 = Label(top)
Label6.place(relx=0.14, rely=0.62, height=21, width=36)
Label6.configure(text='''Type''')

Entry6 = Entry(top)
Entry6.place(relx=0.33, rely=0.62,height=23, relwidth=0.45)
Entry6.configure(background="white") 
Entry6.configure(textvariable=typeVar)

Label7 = Label(top)
Label7.place(relx=0.14, rely=0.71, height=21, width=42)
Label7.configure(text='''Notes''')

Text1 = Text(top)
Text1.place(relx=0.33, rely=0.71, relheight=0.16, relwidth=0.23)
Text1.configure(background="white")
Text1.configure(width=10)
Text1.configure(wrap=WORD) 

Button1 = Button(top)
Button1.place(relx=0.6, rely=0.91, height=29, width=51)
Button1.configure(text='''Add''')
Button1.configure(command=save)

top.mainloop()

