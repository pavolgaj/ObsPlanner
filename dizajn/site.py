import sys

from tkinter import * 
import tkinter.ttk as ttk
from tkinter import messagebox 

import stars

class site():
    def __init__(self,name,lat,lon,ele):
        self.name=name
        self.lat=lat
        self.lon=lon
        self.ele=ele

def saveSite():
    try:
        if ':' in siteLatVar.get(): lat=stars.readDMS(siteLatVar.get(),deg=True)
        else: lat=float(siteLatVar.get())
    except: 
        messagebox.showerror('Latitude Error','Wrong Latitude format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
        return
    try:
        if ':' in siteLonVar.get(): lon=stars.readDMS(siteLonVar.get(),deg=True)
        else: lon=float(siteLonVar.get())
    except: 
        messagebox.showerror('Longitude Error','Wrong Longitude format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
        return    
    sit=site(siteNameVar.get(),lat,lon,float(siteEleVar.get()))    
    topSite.destroy()

topSite=Tk()
topSite.geometry('230x200')
topSite.title('Site')

siteNameVar=StringVar(topSite)
siteLatVar=StringVar(topSite)
siteLonVar=StringVar(topSite)
siteEleVar=StringVar(topSite)

Label1=Label(topSite)
Label1.place(relx=0.05,rely=0.05,height=21,width=43)
Label1.configure(text='Name')
Label1.configure(anchor='w')

Entry1=Entry(topSite)
Entry1.place(relx=0.35,rely=0.05,height=25,relwidth=0.6)
Entry1.configure(background='white')
Entry1.configure(textvariable=siteNameVar)

Label2=Label(topSite)
Label2.place(relx=0.05,rely=0.25,height=21,width=57)
Label2.configure(text='Latitude')
Label2.configure(anchor='w')

Entry2=Entry(topSite)
Entry2.place(relx=0.35,rely=0.25,height=25,relwidth=0.6)
Entry2.configure(background='white')
Entry2.configure(textvariable=siteLatVar)

Label3=Label(topSite)
Label3.place(relx=0.05,rely=0.45,height=21,width=68)
Label3.configure(text='Longitude')
Label3.configure(anchor='w')

Entry3=Entry(topSite)
Entry3.place(relx=0.35,rely=0.45,height=25,relwidth=0.6)
Entry3.configure(background='white')
Entry3.configure(textvariable=siteLonVar)

Label4=Label(topSite)
Label4.place(relx=0.05,rely=0.65,height=21,width=65)
Label4.configure(text='Elevation')
Label4.configure(anchor='w')

Entry4=Entry(topSite)
Entry4.place(relx=0.35,rely=0.65,height=25,relwidth=0.6)
Entry4.configure(background='white')
Entry4.configure(textvariable=siteEleVar)

Button1=Button(topSite)
Button1.place(relx=0.4,rely=0.82,height=29,width=58)
Button1.configure(text='Save')
Button1.configure(command=saveSite)

mainloop()


