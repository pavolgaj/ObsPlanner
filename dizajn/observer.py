import sys

from tkinter import *

import tkinter.ttk as ttk

def saveObs():
    topObs.destroy()

topObs=Tk()
topObs.geometry('300x80')
topObs.title('Observer')

obsNameVar=StringVar(topObs)

Label1=Label(topObs)
Label1.place(relx=0.01,rely=0.1,height=21,width=43)
Label1.configure(text='Name')

Entry1=Entry(topObs)
Entry1.place(relx=0.2,rely=0.1,height=25,relwidth=0.75)
Entry1.configure(background='white')
Entry1.configure(textvariable=obsNameVar)

Button1=Button(topObs)
Button1.place(relx=0.4,rely=0.6,height=24,width=60)
Button1.configure(text='Save')
Button1.configure(command=saveObs)

topObs.mainloop()


