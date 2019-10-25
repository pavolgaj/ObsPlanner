import sys

from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox 

import stars

class siteClass():
    def __init__(self,name,lat,lon,ele):
        self.name=name
        self.lat=lat
        self.lon=lon
        self.ele=ele

def addObserver(obs=None):
    def saveObs():
        if obs is not None: settings['observers'].remove(obs)
        settings['observers'].append(obsNameVar.get())
        TCombobox1['values']=sorted(settings['observers'])
        TCombobox1.current(sorted(settings['observers']).index(obsNameVar.get()))
        topObs.destroy()
    
    topObs=Tk()
    topObs.geometry('300x80')
    topObs.title('Observer')
    
    obsNameVar=StringVar(topObs)
    
    if obs is not None: obsNameVar.set(obs)
    
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
    
def editObserver():
    addObserver(observerVar.get())
    
def delObserver():
    settings['observers'].remove(observerVar.get())
    TCombobox1['values']=sorted(settings['observers'])
    TCombobox1.current(0)
        
def addSite(site=None):
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
  
        if site is not None: del settings['sites'][site]
        settings['sites'][siteNameVar.get()]=siteClass(siteNameVar.get(),lat,lon,float(siteEleVar.get()))
        TCombobox2['values']=sorted(settings['sites'].keys())
        TCombobox2.current(sorted(settings['sites'].keys()).index(siteNameVar.get()))
        topSite.destroy()
    
    topSite=Tk()
    topSite.geometry('230x200')
    topSite.title('Site')
    
    siteNameVar=StringVar(topSite)
    siteLatVar=StringVar(topSite)
    siteLonVar=StringVar(topSite)
    siteEleVar=StringVar(topSite)
    
    if site is not None: 
        siteNameVar.set(site)
        siteLatVar.set(stars.printDMS(settings['sites'][site].lat))
        siteLonVar.set(stars.printDMS(settings['sites'][site].lon))
        siteEleVar.set(settings['sites'][site].ele)
    
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
        
def editSite():
    addSite(siteVar.get())
        
def delSite():
    del settings['sites'][siteVar.get()]
    TCombobox2['values']=sorted(settings['sites'])
    TCombobox2.current(0)
        
def addTel(tel=None):
    def saveTel():
        if tel is not None: settings['telescopes'].remove(tel)
        settings['telescopes'].append(telNameVar.get())
        TCombobox3['values']=sorted(settings['telescopes'])
        TCombobox3.current(sorted(settings['telescopes']).index(telNameVar.get()))
        topTel.destroy()
    
    topTel=Tk()
    topTel.geometry('400x80')
    topTel.title('Telescope')
    
    telNameVar=StringVar(topTel)
    
    if tel is not None: telNameVar.set(tel)
    
    Label1=Label(topTel)
    Label1.place(relx=0.01,rely=0.1,height=21,width=43)
    Label1.configure(text='Name')
    
    Entry1=Entry(topTel)
    Entry1.place(relx=0.15,rely=0.1,height=25,relwidth=0.82)
    Entry1.configure(background='white')
    Entry1.configure(textvariable=telNameVar)
    
    Button1=Button(topTel)
    Button1.place(relx=0.4,rely=0.6,height=24,width=60)
    Button1.configure(text='Save')
    Button1.configure(command=saveTel)
        
def editTel():
    addTel(telVar.get())
        
def delTel():
    settings['telescopes'].remove(telVar.get())
    TCombobox3['values']=sorted(settings['telescopes'])
    TCombobox3.current(0)
        
def saveSet():
    settings['default_obs']=observerVar.get()
    settings['default_site']=settings['sites'][siteVar.get()]
    settings['default_tel']=telVar.get()
    top.destroy()

settings={}
settings['observers']=[]
settings['sites']={}
settings['telescopes']=[]
settings['default_obs']=''
settings['default_site']=''
settings['default_tel']=''
        
top=Tk()
top.geometry('500x150')
top.title('Settings')

observerVar=StringVar(top)
siteVar=StringVar(top)
telVar=StringVar(top)

Label1=Label(top)
Label1.place(relx=0.02,rely=0.02,height=21,width=111)
Label1.configure(text='Default Observer')
Label1.configure(anchor='w')

TCombobox1=ttk.Combobox(top)
TCombobox1.place(relx=0.26,rely=0.02,height=25,relwidth=0.4)
TCombobox1.configure(textvariable=observerVar)
TCombobox1.configure(takefocus='')
TCombobox1.configure(state='readonly')

Button1=Button(top)
Button1.place(relx=0.69,rely=0.02,height=24,width=43)
Button1.configure(text='Add')
Button1.configure(command=addObserver)

Button1_1=Button(top)
Button1_1.place(relx=0.79,rely=0.02,height=24,width=43)
Button1_1.configure(text='Edit')
Button1_1.configure(command=editObserver) 

Button1_2=Button(top)
Button1_2.place(relx=0.89,rely=0.02,height=24,width=43)
Button1_2.configure(text='Delete') 
Button1_2.configure(command=delObserver)

Label2=Label(top)
Label2.place(relx=0.02,rely=0.22,height=21,width=78)
Label2.configure(text='Default Site')
Label2.configure(anchor='w')

TCombobox2=ttk.Combobox(top)
TCombobox2.place(relx=0.26,rely=0.22,height=25,relwidth=0.4)
TCombobox2.configure(textvariable=siteVar)
TCombobox2.configure(takefocus='')
TCombobox2.configure(state='readonly')

Button2=Button(top)
Button2.place(relx=0.69,rely=0.22,height=24,width=43)
Button2.configure(text='Add')
Button2.configure(command=addSite)

Button2_1=Button(top)
Button2_1.place(relx=0.79,rely=0.22,height=24,width=43)
Button2_1.configure(text='Edit')
Button2_1.configure(command=editSite)

Button2_2=Button(top)
Button2_2.place(relx=0.89,rely=0.22,height=24,width=43)
Button2_2.configure(text='Delete')
Button2_2.configure(command=delSite)

Label3=Label(top)
Label3.place(relx=0.02,rely=0.42,height=21,width=118)
Label3.configure(text='Default Technique')
Label3.configure(anchor='w')

TCombobox3=ttk.Combobox(top)
TCombobox3.place(relx=0.26,rely=0.42,height=25,relwidth=0.4)
TCombobox3.configure(textvariable=telVar)
TCombobox3.configure(takefocus='')
TCombobox3.configure(state='readonly')

Button3=Button(top)
Button3.place(relx=0.69,rely=0.42,height=24,width=43)
Button3.configure(text='Add')
Button3.configure(command=addTel)

Button3_1=Button(top)
Button3_1.place(relx=0.79,rely=0.42,height=24,width=43)
Button3_1.configure(text='Edit')
Button3_1.configure(command=editTel)

Button3_2=Button(top)
Button3_2.place(relx=0.89,rely=0.42,height=24,width=43)
Button3_2.configure(text='Delete')
Button3_2.configure(command=delTel)

Label4=Label(top)
Label4.place(relx=0.02,rely=0.62,height=21,width=78)
Label4.configure(text='Image Path')
Label4.configure(anchor='w')

Radiobutton1=Radiobutton(top)
Radiobutton1.place(relx=0.26,rely=0.65,height=21,relwidth=0.15)
Radiobutton1.configure(justify=LEFT)
Radiobutton1.configure(text='Original')

Radiobutton2=Radiobutton(top)
Radiobutton2.place(relx=0.46,rely=0.65,height=21,relwidth=0.12)
Radiobutton2.configure(justify=LEFT)
Radiobutton2.configure(text='Copy')

Button4=Button(top)
Button4.place(relx=0.40,rely=0.8,height=24,width=60)
Button4.configure(text='Save')
Button4.configure(command=saveSet)

mainloop()



