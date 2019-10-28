#!/usr/bin/python3
import sys
import os
import pickle

from tkinter import *
from tkinter import messagebox 
from tkinter import filedialog 
import tkinter.ttk as ttk 

import numpy as np
import matplotlib
matplotlib.use('TkAgg')  
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patheffects as PathEffects
import matplotlib.patches as patches

import datetime
 
import stars 
import objects as objClass
from gui_tools import *

class siteClass():
    def __init__(self,name,lat,lon,ele,limits=None):
        self.name=name
        self.lat=lat
        self.lon=lon
        self.ele=ele
        if limits is None: self.limits=[0,90,0,360]     #min_alt,max_alt,min_az,max_az
        else: self.limits=limits

#grafy
figObj=Figure()
figAlt=Figure()

def sort(zoznam):
    #zoradenie objektov->pridanie nul
    objSort=[]
    order={}
    for x in zoznam:
        for i in range(len(x)):
            try: 
                int(x[i])
                break
            except: pass
        order[x[:i]+x[i:].rjust(10,'0')]=x
    for x in sorted(order):
        #print(x)
        objSort.append(order[x])
    return objSort

def sortObs(zoznam):
    #zoradenie pozorovani
    obsSort=[]
    order={}
    for x in zoznam: order[zoznam[x].jd]=x
    for x in sorted(order): obsSort.append(order[x])
    return obsSort    

def About():
    print('About')
    sys.stdout.flush()

def AddObj(obj=None):
    global objects
    
    def save():
        global objects
        #kontrola vstupu
        if len(nameVar.get())==0:
            messagebox.showerror('Name Error','"Name" not given!')
            return
        else: name=nameVar.get().strip()
        try:
            if ':' in raVar.get(): ra=stars.readDMS(raVar.get(),deg=True)
            else: ra=float(raVar.get())
        except: 
            messagebox.showerror('RA Error','Wrong RA format! Correct format is "H:M:S" or "H.h" (decimal number in hours).')
            return
        try:    
            if ':' in decVar.get(): dec=stars.readDMS(decVar.get(),deg=True)
            else: dec=float(decVar.get()) 
        except: 
            messagebox.showerror('DEC Error','Wrong DEC format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')  
            return               
        if len(constVar.get())==0:
            messagebox.showerror('Constelation Error','"Constelation" not given!')
            return
        
        #nacitanie udajov a pridanie objektu 
        note=TextO.get('1.0',END)   
        if obj is None: 
            objects.add(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),typeVar.get().strip(),note.strip(),constVar.get().strip())  
            #objfilter()  
        else: 
            if not name==obj.name: del objects.objects[obj.name] #TODO: nejake upozornenie...
            objects.objects[name]['object']=stars.star(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),typeVar.get().strip(),note.strip(),constVar.get().strip())
        zoznam=objfilter()
        fake=fakeEvt(zoznam.index(name),zoznam)
        objselect(fake)
      
        top.destroy()
        
    def detect():
        constVar.set('')
        try:
            if ':' in raVar.get(): ra=stars.readDMS(raVar.get(),deg=True)
            else: ra=float(raVar.get())
        except: 
            messagebox.showerror('RA Error','Wrong RA format! Correct format is "H:M:S" or "H.h" (decimal number in hours).')
            return
        try:    
            if ':' in decVar.get(): dec=stars.readDMS(decVar.get(),deg=True)
            else: dec=float(decVar.get()) 
        except: 
            messagebox.showerror('DEC Error','Wrong DEC format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')  
            return     
        for const in constellations:
            if constellations[const].testPoint(ra,dec): 
                constVar.set(const)
                return  
                    
    top=Toplevel(root)
    top.geometry('250x350')
    top.title('Object')
    try: top.iconbitmap('ObsPlanner.ico')   #win
    except: pass
    
    nameVar=StringVar(top)
    raVar=StringVar(top)
    decVar=StringVar(top)
    constVar=StringVar(top)
    magVar=StringVar(top)
    sizeVar=StringVar(top)
    typeVar=StringVar(top)
    
    if obj is not None:
        nameVar.set(obj.name)
        raVar.set(stars.printDMS(obj.ra))
        decVar.set(stars.printDMS(obj.dec))
        constVar.set(obj.const)
        magVar.set(obj.mag)
        sizeVar.set(obj.size)
        typeVar.set(obj.type)
    
    #objekty
    Label1=Label(top)
    Label1.place(relx=0.01,rely=0.02,height=21,width=43)
    Label1.configure(text='Name')
    Label1.configure(anchor='w')
    
    Entry1=Entry(top)
    Entry1.place(relx=0.2,rely=0.02,height=25,relwidth=0.75)
    Entry1.configure(background='white')
    Entry1.configure(textvariable=nameVar)
    
    Label2=Label(top)
    Label2.place(relx=0.01,rely=0.10,height=21,width=43)
    Label2.configure(text='RA')
    Label2.configure(anchor='w')
    
    Entry2=Entry(top)
    Entry2.place(relx=0.2,rely=0.10,height=25,relwidth=0.75)
    Entry2.configure(background='white')
    Entry2.configure(textvariable=raVar)
    
    Label3=Label(top)
    Label3.place(relx=0.01,rely=0.18,height=21,width=43)
    Label3.configure(text='DEC')
    Label3.configure(anchor='w')
    
    Entry3=Entry(top)
    Entry3.place(relx=0.2,rely=0.18,height=25,relwidth=0.75)
    Entry3.configure(background='white')
    Entry3.configure(textvariable=decVar)
    
    Label8=Label(top)
    Label8.place(relx=0.01,rely=0.26,height=21,width=90)
    Label8.configure(text='Constellation')
    Label8.configure(anchor='w')
    
    Entry7=Entry(top)
    Entry7.place(relx=0.4,rely=0.26,height=25,relwidth=0.35)
    Entry7.configure(background='white')
    Entry7.configure(textvariable=constVar)
    
    Button2=Button(top)
    Button2.place(relx=0.76,rely=0.26,height=24,width=47)
    Button2.configure(text='Detect')
    Button2.configure(command=detect)  
    
    Label4=Label(top)
    Label4.place(relx=0.01,rely=0.34,height=21,width=43)
    Label4.configure(text='Mag')
    Label4.configure(anchor='w')
    
    Entry4=Entry(top)
    Entry4.place(relx=0.2,rely=0.34,height=25,relwidth=0.75)
    Entry4.configure(background='white') 
    Entry4.configure(textvariable=magVar)
    
    Label5=Label(top)
    Label5.place(relx=0.01,rely=0.42,height=21,width=43)
    Label5.configure(text='Size')
    Label5.configure(anchor='w')
    
    Entry5=Entry(top)
    Entry5.place(relx=0.2,rely=0.42,height=25,relwidth=0.75)
    Entry5.configure(background='white') 
    Entry5.configure(textvariable=sizeVar) 
    
    Label6=Label(top)
    Label6.place(relx=0.01,rely=0.50,height=21,width=43)
    Label6.configure(text='Type')
    Label6.configure(anchor='w')
    
    Entry6=Entry(top)
    Entry6.place(relx=0.2,rely=0.50,height=25,relwidth=0.75)
    Entry6.configure(background='white') 
    Entry6.configure(textvariable=typeVar)
    
    Label7=Label(top)
    Label7.place(relx=0.01,rely=0.58,height=21,width=43)
    Label7.configure(text='Notes')
    Label7.configure(anchor='w')
    
    TextO=ScrolledText(top)
    TextO.place(relx=0.2,rely=0.58,relheight=0.33,relwidth=0.75)
    TextO.configure(background='white')
    TextO.configure(width=10)
    TextO.configure(wrap=WORD) 
    
    if obj is not None:
        #vypis info o objekte
        old=sys.stdout
        #redirect output to text field
        sys.stdout=StdoutRedirector(TextO)    
        print(obj.note)
        sys.stdout=old
    
    Button1=Button(top)
    Button1.place(relx=0.45,rely=0.93,height=24,width=47)
    Button1.configure(text='Save')
    Button1.configure(command=save)
    

def AddObs(obs=None):
    #todo...
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
        try: topObs.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        
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
        
            
    def addSite(site=None):  
        def setLimits():
            global limits           
            def saveLims():
                global limits
                limits[0]=minAltVar.get()
                limits[1]=maxAltVar.get()
                limits[2]=minAzmVar.get()
                limits[3]=maxAzmVar.get()
                topLims.destroy()
            
            topLims=Tk()
            topLims.geometry('400x150')
            topLims.title('Limits')
            try: topLims.iconbitmap('ObsPlanner.ico')   #win
            except: pass
        
            minAltVar=DoubleVar(topLims)
            maxAltVar=DoubleVar(topLims)
            minAzmVar=DoubleVar(topLims)
            maxAzmVar=DoubleVar(topLims)
            
            if site is not None: limits=settings['sites'][site].limits
            else: limits=new_limits
            
            minAltVar.set(limits[0])
            maxAltVar.set(limits[1])
            minAzmVar.set(limits[2])
            maxAzmVar.set(limits[3])
            
            Label1=Label(topLims)
            Label1.place(relx=0.25,rely=0.05,height=21,width=43)
            Label1.configure(text='Min')
            Label1.configure(anchor='w')
            
            Label2=Label(topLims)
            Label2.place(relx=0.62,rely=0.05,height=21,width=43)
            Label2.configure(text='Max')
            Label2.configure(anchor='w')
            
            Label3=Label(topLims)
            Label3.place(relx=0.05,rely=0.25,height=21,width=80 )
            Label3.configure(text='Altitude')
            Label3.configure(anchor='w')
        
            Entry1=Entry(topLims)
            Entry1.place(relx=0.25,rely=0.25,height=25,relwidth=0.35)
            Entry1.configure(background='white')
            Entry1.configure(textvariable=minAltVar)
            
            Entry2=Entry(topLims)
            Entry2.place(relx=0.62,rely=0.25,height=25,relwidth=0.35)
            Entry2.configure(background='white')
            Entry2.configure(textvariable=maxAltVar)
            
            Label4=Label(topLims)
            Label4.place(relx=0.05,rely=0.45,height=21,width=80)
            Label4.configure(text='Azimut')
            Label4.configure(anchor='w')
            
            Entry3=Entry(topLims)
            Entry3.place(relx=0.25,rely=0.45,height=25,relwidth=0.35)
            Entry3.configure(background='white')
            Entry3.configure(textvariable=minAzmVar)
            
            Entry4=Entry(topLims)
            Entry4.place(relx=0.62,rely=0.45,height=25,relwidth=0.35)
            Entry4.configure(background='white')
            Entry4.configure(textvariable=maxAzmVar)
            
            Button2=Button(topLims)
            Button2.place(relx=0.45,rely=0.7,height=29,width=58)
            Button2.configure(text='Save')
            Button2.configure(command=saveLims) 
            
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
            settings['sites'][siteNameVar.get()]=siteClass(siteNameVar.get(),lat,lon,float(siteEleVar.get()),limits)
            TCombobox2['values']=sorted(settings['sites'].keys())
            TCombobox2.current(sorted(settings['sites'].keys()).index(siteNameVar.get()))
            topSite.destroy()
        
        topSite=Tk()
        topSite.geometry('230x200')
        topSite.title('Site')
        try: topSite.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        
        siteNameVar=StringVar(topSite)
        siteLatVar=StringVar(topSite)
        siteLonVar=StringVar(topSite)
        siteEleVar=StringVar(topSite) 
        new_limits=[0,90,0,360] 
        limits=new_limits       
        
        if site is not None: 
            siteNameVar.set(site)
            siteLatVar.set(stars.printDMS(settings['sites'][site].lat))
            siteLonVar.set(stars.printDMS(settings['sites'][site].lon))
            siteEleVar.set(settings['sites'][site].ele)
            limits=settings['sites'][site].limits
        
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
        Button1.place(relx=0.2,rely=0.82,height=29,width=58)
        Button1.configure(text='Limits')
        Button1.configure(command=setLimits)  
        
        Button2=Button(topSite)
        Button2.place(relx=0.6,rely=0.82,height=29,width=58)
        Button2.configure(text='Save')
        Button2.configure(command=saveSite)     
            
    def editSite():
        addSite(siteVar.get())
            
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
        try: topTel.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        
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
    
    def addObsObj(obj=None):                                                                
        def save():
            #kontrola vstupu
            if len(nameVar.get())==0:
                messagebox.showerror('Name Error','"Name" not given!')
                return
            else: name=nameVar.get().strip()
            try:
                if ':' in raVar.get(): ra=stars.readDMS(raVar.get(),deg=True)
                else: ra=float(raVar.get())
            except: 
                messagebox.showerror('RA Error','Wrong RA format! Correct format is "H:M:S" or "H.h" (decimal number in hours).')
                return
            try:    
                if ':' in decVar.get(): dec=stars.readDMS(decVar.get(),deg=True)
                else: dec=float(decVar.get()) 
            except: 
                messagebox.showerror('DEC Error','Wrong DEC format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')  
                return               
            if len(constVar.get())==0:
                messagebox.showerror('Constelation Error','"Constelation" not given!')
                return
            
            #nacitanie udajov a pridanie objektu 
            note=TextO.get('1.0',END)   
            if obj is None: 
                objects.add(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),typeVar.get().strip(),note.strip(),constVar.get().strip())  
            else: 
                if not name==obj.name: del objects.objects[obj.name] #TODO: nejake upozornenie...
                objects.objects[name]['object']=stars.star(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),typeVar.get().strip(),note.strip(),constVar.get().strip())
            #todo: ak nie je observed...
            zoznam=objfilter()
            fake=fakeEvt(zoznam.index(name),zoznam)
            objselect(fake)
            
            TCombobox4['values']=sort(objects.objects.keys())
            TCombobox4.current(sort(objects.objects.keys()).index(objZ.name))
          
            topObj.destroy()
            
        def detect():
            constVar.set('')
            try:
                if ':' in raVar.get(): ra=stars.readDMS(raVar.get(),deg=True)
                else: ra=float(raVar.get())
            except: 
                messagebox.showerror('RA Error','Wrong RA format! Correct format is "H:M:S" or "H.h" (decimal number in hours).')
                return
            try:    
                if ':' in decVar.get(): dec=stars.readDMS(decVar.get(),deg=True)
                else: dec=float(decVar.get()) 
            except: 
                messagebox.showerror('DEC Error','Wrong DEC format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')  
                return     
            for const in constellations:
                if constellations[const].testPoint(ra,dec): 
                    constVar.set(const)
                    return  
                        
        topObj=Toplevel(root)
        topObj.geometry('250x350')
        topObj.title('Object')
        try: topObj.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        
        nameVar=StringVar(topObj)
        raVar=StringVar(topObj)
        decVar=StringVar(topObj)
        constVar=StringVar(topObj)
        magVar=StringVar(topObj)
        sizeVar=StringVar(topObj)
        typeVar=StringVar(topObj)
        
        if obj is not None:
            nameVar.set(obj.name)
            raVar.set(stars.printDMS(obj.ra))
            decVar.set(stars.printDMS(obj.dec))
            constVar.set(obj.const)
            magVar.set(obj.mag)
            sizeVar.set(obj.size)
            typeVar.set(obj.type)
        
        #objekty
        Label1=Label(topObj)
        Label1.place(relx=0.01,rely=0.02,height=21,width=43)
        Label1.configure(text='Name')
        Label1.configure(anchor='w')
        
        Entry1=Entry(topObj)
        Entry1.place(relx=0.2,rely=0.02,height=25,relwidth=0.75)
        Entry1.configure(background='white')
        Entry1.configure(textvariable=nameVar)
        
        Label2=Label(topObj)
        Label2.place(relx=0.01,rely=0.10,height=21,width=43)
        Label2.configure(text='RA')
        Label2.configure(anchor='w')
        
        Entry2=Entry(topObj)
        Entry2.place(relx=0.2,rely=0.10,height=25,relwidth=0.75)
        Entry2.configure(background='white')
        Entry2.configure(textvariable=raVar)
        
        Label3=Label(topObj)
        Label3.place(relx=0.01,rely=0.18,height=21,width=43)
        Label3.configure(text='DEC')
        Label3.configure(anchor='w')
        
        Entry3=Entry(topObj)
        Entry3.place(relx=0.2,rely=0.18,height=25,relwidth=0.75)
        Entry3.configure(background='white')
        Entry3.configure(textvariable=decVar)
        
        Label8=Label(topObj)
        Label8.place(relx=0.01,rely=0.26,height=21,width=90)
        Label8.configure(text='Constellation')
        Label8.configure(anchor='w')
        
        Entry7=Entry(topObj)
        Entry7.place(relx=0.4,rely=0.26,height=25,relwidth=0.35)
        Entry7.configure(background='white')
        Entry7.configure(textvariable=constVar)
        
        Button2=Button(topObj)
        Button2.place(relx=0.76,rely=0.26,height=24,width=47)
        Button2.configure(text='Detect')
        Button2.configure(command=detect)  
        
        Label4=Label(topObj)
        Label4.place(relx=0.01,rely=0.34,height=21,width=43)
        Label4.configure(text='Mag')
        Label4.configure(anchor='w')
        
        Entry4=Entry(topObj)
        Entry4.place(relx=0.2,rely=0.34,height=25,relwidth=0.75)
        Entry4.configure(background='white') 
        Entry4.configure(textvariable=magVar)
        
        Label5=Label(topObj)
        Label5.place(relx=0.01,rely=0.42,height=21,width=43)
        Label5.configure(text='Size')
        Label5.configure(anchor='w')
        
        Entry5=Entry(topObj)
        Entry5.place(relx=0.2,rely=0.42,height=25,relwidth=0.75)
        Entry5.configure(background='white') 
        Entry5.configure(textvariable=sizeVar) 
        
        Label6=Label(topObj)
        Label6.place(relx=0.01,rely=0.50,height=21,width=43)
        Label6.configure(text='Type')
        Label6.configure(anchor='w')
        
        Entry6=Entry(topObj)
        Entry6.place(relx=0.2,rely=0.50,height=25,relwidth=0.75)
        Entry6.configure(background='white') 
        Entry6.configure(textvariable=typeVar)
        
        Label7=Label(topObj)
        Label7.place(relx=0.01,rely=0.58,height=21,width=43)
        Label7.configure(text='Notes')
        Label7.configure(anchor='w')
        
        TextO=ScrolledText(topObj)
        TextO.place(relx=0.2,rely=0.58,relheight=0.33,relwidth=0.75)
        TextO.configure(background='white')
        TextO.configure(width=10)
        TextO.configure(wrap=WORD) 
        
        if obj is not None:
            #vypis info o objekte
            old=sys.stdout
            #redirect output to text field
            sys.stdout=StdoutRedirector(TextO)    
            print(obj.note)
            sys.stdout=old
        
        Button1=Button(topObj)
        Button1.place(relx=0.45,rely=0.93,height=24,width=47)
        Button1.configure(text='Save')
        Button1.configure(command=save)  

        
        
    def edObsObj():
        addObsObj(objects.objects[objVar.get()]['object'])   
    
    def saveObs():
        #todo testovanie...
        note=TextO.get('1.0',END)
        try: dt=datetime.datetime.strptime(obsDateVar.get(),'%Y-%m-%d %H:%M:%S')
        except: 
            messagebox.showerror('Date/Time Error','Wrong date/time format! Correct format is "Y-m-d H:M:S". Date/time set to current time.')
            return
        #todo zmena datumu
        objects.addObs(objVar.get(),dt,observerVar.get(),telVar.get(),settings['sites'][siteVar.get()],image='',note=note.strip())       
                
        zoznam=objfilter()
        fake=fakeEvt(zoznam.index(objVar.get()),zoznam)
        objselect(fake)
        
        zoznam=sortObs(obsZ)
        fake=fakeEvt(zoznam.index(obsDateVar.get()),zoznam)
        obsselect(fake)
        
        top.destroy()
    
    top=Tk()
    top.geometry('450x400')
    top.title('Observation') 
    try: top.iconbitmap('ObsPlanner.ico')   #win
    except: pass
    
    observerVar=StringVar(top)
    siteVar=StringVar(top)
    telVar=StringVar(top)
    objVar=StringVar(top)
    obsDateVar=StringVar(top)
    
    obsDateVar.set(dateVar.get())
    
    Label1=Label(top)
    Label1.place(relx=0.02,rely=0.02,height=21,width=63)
    Label1.configure(text='Observer')
    Label1.configure(anchor='w')
    
    TCombobox1=ttk.Combobox(top)
    TCombobox1.place(relx=0.27,rely=0.02,height=25,relwidth=0.45) 
    TCombobox1.configure(textvariable=observerVar)
    TCombobox1.configure(takefocus='')
    TCombobox1.configure(state='readonly')
    if len(settings['observers'])>0:
        TCombobox1['values']=sorted(settings['observers'])
        TCombobox1.current(sorted(settings['observers']).index(settings['default_obs']))
    
    ButtonOA=Button(top)
    ButtonOA.place(relx=0.75,rely=0.02,height=24,width=43)
    ButtonOA.configure(text='Add')
    ButtonOA.configure(command=addObserver)
    
    ButtonOE=Button(top)
    ButtonOE.place(relx=0.88,rely=0.02,height=24,width=43)
    ButtonOE.configure(text='Edit')
    ButtonOE.configure(command=editObserver)
    
    Label2=Label(top)
    Label2.place(relx=0.02,rely=0.10,height=21,width=130)
    Label2.configure(text='UTC Date/Time')
    Label2.configure(anchor='w')
    
    Entry1=Entry(top)
    Entry1.place(relx=0.27,rely=0.10,height=25,relwidth=0.45)
    Entry1.configure(background='white')
    Entry1.configure(textvariable=obsDateVar)
    
    Label3=Label(top)
    Label3.place(relx=0.02,rely=0.18,height=21,width=29)
    Label3.configure(text='Site')
    Label3.configure(anchor='w')
    
    TCombobox2=ttk.Combobox(top)
    TCombobox2.place(relx=0.27,rely=0.18,height=25,relwidth=0.45) 
    TCombobox2.configure(textvariable=siteVar)
    TCombobox2.configure(takefocus='')
    TCombobox2.configure(state='readonly')
    if len(settings['sites'])>0:
        TCombobox2['values']=sorted(settings['sites'])
        TCombobox2.current(sorted(settings['sites']).index(settings['default_site'].name))
    
    ButtonOA=Button(top)
    ButtonOA.place(relx=0.75,rely=0.18,height=25,width=43)
    ButtonOA.configure(text='Add')
    ButtonOA.configure(command=addSite)
    
    ButtonOE=Button(top)
    ButtonOE.place(relx=0.88,rely=0.18,height=25,width=43)
    ButtonOE.configure(text='Edit')
    ButtonOE.configure(command=editSite)
    
    Label4=Label(top)
    Label4.place(relx=0.02,rely=0.26,height=21,width=75)
    Label4.configure(text='Telescope')
    Label4.configure(anchor='w')
    
    TCombobox3=ttk.Combobox(top)
    TCombobox3.place(relx=0.27,rely=0.26,height=25,relwidth=0.45) 
    TCombobox3.configure(textvariable=telVar)
    TCombobox3.configure(takefocus='')
    TCombobox3.configure(state='readonly')
    if len(settings['telescopes'])>0:
        TCombobox3['values']=sorted(settings['telescopes'])
        TCombobox3.current(sorted(settings['telescopes']).index(settings['default_tel']))
    
    ButtonOA=Button(top)
    ButtonOA.place(relx=0.75,rely=0.26,height=25,width=43)
    ButtonOA.configure(text='Add')
    ButtonOA.configure(command=addTel)
    
    ButtonOE=Button(top)
    ButtonOE.place(relx=0.88,rely=0.26,height=25,width=43)
    ButtonOE.configure(text='Edit')
    ButtonOE.configure(command=editTel)
    
    Label5=Label(top)
    Label5.place(relx=0.02,rely=0.34,height=21,width=46)
    Label5.configure(text='Object')
    Label5.configure(anchor='w')
    
    TCombobox4=ttk.Combobox(top)
    TCombobox4.place(relx=0.27,rely=0.34,height=25,relwidth=0.45)
    TCombobox4.configure(textvariable=objVar)
    TCombobox4.configure(takefocus='')
    TCombobox4.configure(state='readonly')
    if len(objects.objects.keys())>0:
        TCombobox4['values']=sort(objects.objects.keys())
        TCombobox4.current(sort(objects.objects.keys()).index(objZ.name))
    
    ButtonObA=Button(top)
    ButtonObA.place(relx=0.75,rely=0.34,height=25,width=43)
    ButtonObA.configure(text='Add')
    ButtonObA.configure(command=addObsObj)
    
    ButtonObE=Button(top)
    ButtonObE.place(relx=0.88,rely=0.34,height=25,width=43)
    ButtonObE.configure(text='Edit')
    ButtonObE.configure(command=edObsObj)
    
    Label6=Label(top)
    Label6.place(relx=0.02,rely=0.42,height=21,width=45)
    Label6.configure(text='Image')
    Label6.configure(state=DISABLED)
    Label6.configure(anchor='w')
    
    Entry2=Entry(top)
    Entry2.place(relx=0.27,rely=0.42,height=25,relwidth=0.45)
    Entry2.configure(background='white')
    Entry2.configure(state=DISABLED)   
    
    Button1=Button(top)
    Button1.place(relx=0.75,rely=0.42,height=25,width=43)
    Button1.configure(text='Add')
    Button1.configure(state=DISABLED)
    
    Label7=Label(top)
    Label7.place(relx=0.02,rely=0.5,height=21,width=46)
    Label7.configure(text='Note')
    Label7.configure(anchor='w')
    
    TextO=ScrolledText(top)
    TextO.place(relx=0.27,rely=0.5,relheight=0.35,relwidth=0.45)
    TextO.configure(background='white')
    TextO.configure(width=10)
    TextO.configure(wrap=WORD) 
    
    Button2=Button(top)
    Button2.place(relx=0.38,rely=0.88,height=29,width=57)
    Button2.configure(text='Save')
    Button2.configure(command=saveObs)
            
    if obs is not None:
        observerVar.set(obs.observer)
        siteVar.set(obs.site.name)
        telVar.set(obs.telescope)
        objVar.set(obs.obj)
        obsDateVar.set(obs.date)
        
        #vypis info o objekte
        old=sys.stdout
        #redirect output to text field
        sys.stdout=StdoutRedirector(TextO)    
        print(obs.note)
        sys.stdout=old
        

def DelObj():
    #TODO: potvrdenie o zmazani
    del objects.objects[objZ.name]    
    objfilter()
    obssVar.set('')
    Text1.delete(1.0,END)
    Text2.delete(1.0,END)
    figAlt.clf()
    figObj.clf()
    canvas1.draw()
    canvas2.draw()
    #TODO: blokovanie tlacidiel
    Button2.configure(state=DISABLED)
    Button3.configure(state=DISABLED)
    Button4.configure(state=DISABLED)
    Button5.configure(state=DISABLED)
    Button6.configure(state=DISABLED)

def DelObs():
    del objects.objects[objZ.name]['obs'][obsZ1.date]
    obsZ=objects.objects[objZ.name]['obs']
    
    Text2.delete(1.0,END)
    obssVar.set(sortObs(obsZ))
    Button5.configure(state=DISABLED)
    Button6.configure(state=DISABLED)

def EditObj():
    AddObj(objZ)      

def EditObs():
    AddObs(obsZ1)

def Exit(): 
    global root
    if not noSett:
        f=open('data/settings.ops','wb')
        pickle.dump(settings,f)
        f.close()
    
    root.destroy()
    root=None
    matplotlib.pyplot.close()
    #todo save?

def NewFile():
    global objects      
    objects=objClass.objects(constellations)
    objfilter()
    obssVar.set('')
    Text1.delete(1.0,END)
    Text2.delete(1.0,END)
    figAlt.clf()
    figObj.clf()
    canvas1.draw()
    canvas2.draw()
    settings['file']=''
    #TODO: disable edit,delete,image
    Button2.configure(state=DISABLED)
    Button3.configure(state=DISABLED)
    Button4.configure(state=DISABLED)
    Button5.configure(state=DISABLED)
    Button6.configure(state=DISABLED)

def NowTime():
    dt=datetime.datetime.now(datetime.timezone.utc)
    dateVar.set(dt.strftime('%Y-%m-%d %H:%M:%S'))

def OpenFile():
    global objects 
    name=filedialog.askopenfilename(parent=root,filetypes=[('ObsPlanner files','*.opd'),('All files','*.*')],title='Open file')
    name=name.replace('\\','/')        
    
    if len(name)>0:                   
        objects=objClass.objects(constellations)          
        objects.load(name)          
        objfilter()
        obssVar.set('')
        Text1.delete(1.0,END)
        Text2.delete(1.0,END)
        figAlt.clf()
        figObj.clf()
        canvas1.draw()
        canvas2.draw()
        cwd=os.getcwd().replace('\\','/')+'/'
        if cwd in name: name=name.replace(cwd,'')    #uloz relativnu cestu
        settings['file']=name         
        Button2.configure(state=DISABLED)
        Button3.configure(state=DISABLED)
        Button4.configure(state=DISABLED)
        Button5.configure(state=DISABLED)
        Button6.configure(state=DISABLED)

def SaveFile():
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('ObsPlanner files','*.opd'),('All files','*.*')],title='Save file',defaultextension='.opd')         
    name=name.replace('\\','/')
    if len(name)>0: 
        objects.save(name)
        cwd=os.getcwd().replace('\\','/')+'/'
        if cwd in name: name=name.replace(cwd,'')    #uloz relativnu cestu
        settings['file']=name

def Settings():
    #TODO: blokovanie tlacidiel
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
        try: topObs.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        
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
        def setLimits():
            global limits           
            def saveLims():
                global limits
                limits[0]=minAltVar.get()
                limits[1]=maxAltVar.get()
                limits[2]=minAzmVar.get()
                limits[3]=maxAzmVar.get()
                topLims.destroy()
            
            topLims=Tk()
            topLims.geometry('400x150')
            topLims.title('Limits')
            try: topLims.iconbitmap('ObsPlanner.ico')   #win
            except: pass
        
            minAltVar=DoubleVar(topLims)
            maxAltVar=DoubleVar(topLims)
            minAzmVar=DoubleVar(topLims)
            maxAzmVar=DoubleVar(topLims)
            
            if site is not None: limits=settings['sites'][site].limits
            else: limits=new_limits
            
            minAltVar.set(limits[0])
            maxAltVar.set(limits[1])
            minAzmVar.set(limits[2])
            maxAzmVar.set(limits[3])
            
            Label1=Label(topLims)
            Label1.place(relx=0.25,rely=0.05,height=21,width=43)
            Label1.configure(text='Min')
            Label1.configure(anchor='w')
            
            Label2=Label(topLims)
            Label2.place(relx=0.62,rely=0.05,height=21,width=43)
            Label2.configure(text='Max')
            Label2.configure(anchor='w')
            
            Label3=Label(topLims)
            Label3.place(relx=0.05,rely=0.25,height=21,width=80 )
            Label3.configure(text='Altitude')
            Label3.configure(anchor='w')
        
            Entry1=Entry(topLims)
            Entry1.place(relx=0.25,rely=0.25,height=25,relwidth=0.35)
            Entry1.configure(background='white')
            Entry1.configure(textvariable=minAltVar)
            
            Entry2=Entry(topLims)
            Entry2.place(relx=0.62,rely=0.25,height=25,relwidth=0.35)
            Entry2.configure(background='white')
            Entry2.configure(textvariable=maxAltVar)
            
            Label4=Label(topLims)
            Label4.place(relx=0.05,rely=0.45,height=21,width=80)
            Label4.configure(text='Azimut')
            Label4.configure(anchor='w')
            
            Entry3=Entry(topLims)
            Entry3.place(relx=0.25,rely=0.45,height=25,relwidth=0.35)
            Entry3.configure(background='white')
            Entry3.configure(textvariable=minAzmVar)
            
            Entry4=Entry(topLims)
            Entry4.place(relx=0.62,rely=0.45,height=25,relwidth=0.35)
            Entry4.configure(background='white')
            Entry4.configure(textvariable=maxAzmVar)
            
            Button2=Button(topLims)
            Button2.place(relx=0.45,rely=0.7,height=29,width=58)
            Button2.configure(text='Save')
            Button2.configure(command=saveLims) 
            
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
            settings['sites'][siteNameVar.get()]=siteClass(siteNameVar.get(),lat,lon,float(siteEleVar.get()),limits)
            TCombobox2['values']=sorted(settings['sites'].keys())
            TCombobox2.current(sorted(settings['sites'].keys()).index(siteNameVar.get()))
            topSite.destroy()
        
        topSite=Tk()
        topSite.geometry('230x200')
        topSite.title('Site')
        try: topSite.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        
        siteNameVar=StringVar(topSite)
        siteLatVar=StringVar(topSite)
        siteLonVar=StringVar(topSite)
        siteEleVar=StringVar(topSite) 
        new_limits=[0,90,0,360] 
        limits=new_limits       
        
        if site is not None: 
            siteNameVar.set(site)
            siteLatVar.set(stars.printDMS(settings['sites'][site].lat))
            siteLonVar.set(stars.printDMS(settings['sites'][site].lon))
            siteEleVar.set(settings['sites'][site].ele)
            limits=settings['sites'][site].limits
        
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
        Button1.place(relx=0.2,rely=0.82,height=29,width=58)
        Button1.configure(text='Limits')
        Button1.configure(command=setLimits)  
        
        Button2=Button(topSite)
        Button2.place(relx=0.6,rely=0.82,height=29,width=58)
        Button2.configure(text='Save')
        Button2.configure(command=saveSite)     
            
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
        try: topTel.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        
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
        if len(observerVar.get())==0: 
            messagebox.showerror('Observer Error','No default observer! Please, add one!')
            return
        if len(siteVar.get())==0: 
            messagebox.showerror('Site Error','No default site! Please, add one!')
            return
        if len(telVar.get())==0: 
            messagebox.showerror('Telescope Error','No default telescope! Please, add one!')
            return
        settings['default_obs']=observerVar.get()
        settings['default_site']=settings['sites'][siteVar.get()]
        settings['default_tel']=telVar.get()
        noSett=False  
        
        if len(objects.objects.keys())>0:
            zoznam=objfilter()
            if objZ.name in zoznam:
                fake=fakeEvt(zoznam.index(objZ.name),zoznam)
                objselect(fake)
            else: 
                obssVar.set('')
                Text1.delete(1.0,END)
                Text2.delete(1.0,END)
                figAlt.clf()
                figObj.clf()
                canvas1.draw()
                canvas2.draw()                   
                Button2.configure(state=DISABLED)
                Button3.configure(state=DISABLED)
                Button4.configure(state=DISABLED)
                Button5.configure(state=DISABLED)
                Button6.configure(state=DISABLED)
                
        top.destroy()     
                
    top=Tk()
    top.geometry('500x150')
    top.title('Settings')
    try: top.iconbitmap('ObsPlanner.ico')   #win
    except: pass
    
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
    if len(settings['observers'])>0:
        TCombobox1['values']=sorted(settings['observers'])
        TCombobox1.current(sorted(settings['observers']).index(settings['default_obs']))
    
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
    if len(settings['sites'])>0:
        TCombobox2['values']=sorted(settings['sites'].keys())
        TCombobox2.current(sorted(settings['sites'].keys()).index(settings['default_site'].name))
    
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
    Label3.configure(text='Default Telescope')
    Label3.configure(anchor='w')
    
    TCombobox3=ttk.Combobox(top)
    TCombobox3.place(relx=0.26,rely=0.42,height=25,relwidth=0.4)
    TCombobox3.configure(textvariable=telVar)
    TCombobox3.configure(takefocus='')
    TCombobox3.configure(state='readonly')
    if len(settings['telescopes'])>0:
        TCombobox3['values']=sorted(settings['telescopes'])
        TCombobox3.current(sorted(settings['telescopes']).index(settings['default_tel']))
    
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
    Label4.configure(state=DISABLED)
    
    Radiobutton1=Radiobutton(top)
    Radiobutton1.place(relx=0.26,rely=0.65,height=21,relwidth=0.15)
    Radiobutton1.configure(justify=LEFT)
    Radiobutton1.configure(text='Original')
    Radiobutton1.configure(state=DISABLED)
    
    Radiobutton2=Radiobutton(top)
    Radiobutton2.place(relx=0.46,rely=0.65,height=21,relwidth=0.12)
    Radiobutton2.configure(justify=LEFT)
    Radiobutton2.configure(text='Copy')
    Radiobutton2.configure(state=DISABLED)
    
    Button4=Button(top)
    Button4.place(relx=0.40,rely=0.8,height=24,width=60)
    Button4.configure(text='Save')
    Button4.configure(command=saveSet)

def ShowImg():
    print('ShowImg')
    sys.stdout.flush()
    
def getDate(date=None):
    if date is None: date=dateVar.get()
    try: dt=datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    except: 
        messagebox.showerror('Date/Time Error','Wrong date/time format! Correct format is "Y-m-d H:M:S". Date/time set to current time.')
        NowTime()
    dt=datetime.datetime.strptime(dateVar.get(),'%Y-%m-%d %H:%M:%S')
    return dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second
    

def plotAlt(ra,dec):
    #vykreslenie krivky pozorovatelnosti
    figAlt.clf()
    ax=figAlt.add_subplot(111)
    #vyznacenie limitov
    rect=patches.Rectangle((-10,0),380,100,edgecolor='none',facecolor='lightgray')
    ax.add_patch(rect)
    rect=patches.Rectangle((settings['default_site'].limits[2],settings['default_site'].limits[0]),\
        settings['default_site'].limits[3]-settings['default_site'].limits[2],\
        settings['default_site'].limits[1]-settings['default_site'].limits[0],linewidth=1,edgecolor='gray',facecolor='white')
    ax.add_patch(rect)
    
    year,mon,day,hour,minute,sec=getDate()
    jd0=stars.juldat(year,mon,day,hour-2,minute,sec)  #start -2h
    jd1=stars.juldat(year,mon,day,hour+8,minute,sec)  #stop +8h
    jd=np.linspace(jd0,jd1,200)
    
    a,h=objZ.altAz(jd,settings['default_site'].lon,settings['default_site'].lat)
    if max(h)<0: 
        figAlt.clf()
        ax=figAlt.add_subplot(111)
        ax.text(0,0,'Below horizont!',horizontalalignment='center',verticalalignment='center',fontsize=30)
        ax.set_xlim(-0.5,0.5)
        ax.set_ylim(-0.5,0.5)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(False)
        ax.set_axis_off()
        canvas2.draw()
        return
    h0=h[np.where(h>0)]
    a0=a[np.where(h>0)]
    ax.plot(a0,h0,'k-')
    
    ax.set_xlim(min(a0)-5,max(a0)+5)
    ax.set_ylim(min(h0),max(h)+5) 
    
    #znacky po hodinach
    jdH=np.arange(stars.juldat(year,mon,day,hour-1,0,0),stars.juldat(year,mon,day,hour+7,0,1),1./24.)
    for i in range(len(jdH)):
        a,h=objZ.altAz(jdH[i],settings['default_site'].lon,settings['default_site'].lat)
        if h>0:
            ax.plot(a,h,'ko') 
            if hour-1+i>24: 
                t=ax.text(a,h-max(h0)/10.,hour-2+i-24)
                t.set_path_effects([PathEffects.withStroke(linewidth=2,foreground='w')])
            else: 
                t=ax.text(a,h-max(h0)/10.,hour-1+i)   
                t.set_path_effects([PathEffects.withStroke(linewidth=2,foreground='w')])                  
    
    #aktualna poloha
    jd=stars.juldat(year,mon,day,hour,minute,sec)    
    a,h=objZ.altAz(jd,settings['default_site'].lon,settings['default_site'].lat)
    ax.plot(a,h,'kx',markersize=12)
    
    ax.set_ylabel('Alt. (deg)')
    ax.set_xlabel('Azm. (deg)')
    figAlt.tight_layout()
    canvas2.draw()

def objfilter(event=None):
    #filtre objektov
    filt=filtVar.get()
    zoznam=[]
    if filt=='All': zoznam=objects.objects.keys()
    elif filt=='Visible': 
        year,mon,day,hour,minute,sec=getDate()
        jd=stars.juldat(year,mon,day,hour,minute,sec)
        for ob in objects.objects.values():
            a,h=ob['object'].altAz(jd,settings['default_site'].lon,settings['default_site'].lat)
            if (a<settings['default_site'].limits[3]) and (a>settings['default_site'].limits[2]) and (h<settings['default_site'].limits[1]) and (h>settings['default_site'].limits[0]): 
                zoznam.append(ob['object'].name)
    elif filt=='Above horizont': 
        year,mon,day,hour,minute,sec=getDate()
        jd=stars.juldat(year,mon,day,hour,minute,sec)
        for ob in objects.objects.values():
            a,h=ob['object'].altAz(jd,settings['default_site'].lon,settings['default_site'].lat)
            if (h>0): zoznam.append(ob['object'].name)
    elif filt=='Observed':
        for ob in objects.objects.values():
            if len(ob['obs'])>0: zoznam.append(ob['object'].name)
    elif filt=='Not Observed': 
        for ob in objects.objects.values():
            if len(ob['obs'])==0: zoznam.append(ob['object'].name)
    elif filt=='Visible + Not Observed': 
        year,mon,day,hour,minute,sec=getDate()
        jd=stars.juldat(year,mon,day,hour,minute,sec)
        for ob in objects.objects.values():
            if len(ob['obs'])==0:                
                a,h=ob['object'].altAz(jd,settings['default_site'].lon,settings['default_site'].lat)
                if (a<settings['default_site'].limits[3]) and (a>settings['default_site'].limits[2]) and (h<settings['default_site'].limits[1]) and (h>settings['default_site'].limits[0]): 
                    zoznam.append(ob['object'].name)
    zoznam=sort(zoznam)
    objsVar.set(zoznam)   
    return zoznam    
    
def objselect(evt):
    global objZ,obsZ #zobrazeny objekt a zoznam pozorovani 
    w=evt.widget
    if len(w.curselection())==0: return 
    index=int(w.curselection()[0])
    value=w.get(index)
    
    objZ=objects.objects[value]['object']
    obsZ=objects.objects[value]['obs']
    #vykreslenie polohy v suhv.
    constellations[objZ.const].plotObject(objZ.ra,objZ.dec,figObj)
    canvas1.draw()
    
    plotAlt(objZ.ra,objZ.dec)
    
    year,mon,day,hour,minute,sec=getDate()
    Text1.delete(1.0,END)
    Text2.delete(1.0,END)
    #vypis info o objekte
    old=sys.stdout
    #redirect output to text field
    sys.stdout=StdoutRedirector(Text1)    
    print(objZ.name)
    print('Type: '+objZ.type)
    print('---------------------')
    print('RA: '+stars.printDMS(objZ.ra)+'; DEC: '+stars.printDMS(objZ.dec))
    print('Const.: '+objZ.const)
    print('Size: '+objZ.size)
    print('Mag: '+str(objZ.mag))
    print('---------------------')
    a,h=objZ.altAz(stars.juldat(year,mon,day,hour,minute,sec),settings['default_site'].lon,settings['default_site'].lat)
    print('Az: '+stars.printDMS(a)+'; Alt: '+stars.printDMS(h))
    r,t,s=objZ.rise(stars.juldat(year,mon,day+round(hour/24.),0,0,0),settings['default_site'].lon,settings['default_site'].lat)
    if not r=='NA': 
        r=stars.printDMS(r)
        s=stars.printDMS(s)
    print('Rise: '+r)
    print('Transit: '+stars.printDMS(t))
    print('Set: '+s)
    print('---------------------')
    print('Note: '+objZ.note)
    sys.stdout=old 

    obssVar.set(sortObs(obsZ))
    Button2.configure(state=NORMAL)
    Button3.configure(state=NORMAL)
    Button4.configure(state=NORMAL)
    Button5.configure(state=DISABLED)
    Button6.configure(state=DISABLED)

def obsselect(evt):
    global obsZ1  #zobrazene pozorovanie       
    if len(obsZ)==0: return                
    w=evt.widget
    if len(w.curselection())==0: return
    index=int(w.curselection()[0])
    value=w.get(index)
    
    obsZ1=obsZ[value]    
    Text2.delete(1.0,END)
    #vypis info
    old=sys.stdout
    #redirect output to text field
    sys.stdout=StdoutRedirector(Text2)    
    print(obsZ1.date)   
    print('Observer: '+obsZ1.observer)
    print('Telescope: '+obsZ1.telescope)  
    print('Site: '+obsZ1.site.name) 
    print('---------------------')
    print('Note: '+obsZ1.note)    
    sys.stdout=old 
    
    Button5.configure(state=NORMAL)
    Button6.configure(state=NORMAL)

constellations=stars.load()
objects=objClass.objects(constellations)

#nastavenia
if os.path.isfile('data/settings.ops'): 
    f=open('data/settings.ops','rb')
    settings=pickle.load(f)
    f.close()    
    if os.path.isfile(settings['file'].strip()): objects.load(settings['file'].strip()) 
    noSett=False   
else:
    settings={}
    settings['observers']=[]
    settings['sites']={}
    settings['telescopes']=[]
    settings['default_obs']=''
    settings['default_site']=None
    settings['default_tel']=''
    settings['file']=''
    settings['night_mode']=False
    noSett=True    

root=Tk() 
root.protocol('WM_DELETE_WINDOW',Exit)
try: root.state('zoomed')  #win
except:
    try: root.attributes('-zoomed',True)  #linux
    except: pass

root.geometry('800x500')
root.title('ObsPlanner')  
try: root.iconbitmap('ObsPlanner.ico')   #win
except: pass

#premenne pre gui
objsVar=StringVar(root)
objInfoVar=StringVar(root)
obssVar=StringVar(root)
dateVar=StringVar(root)
filtVar=StringVar(root)      
                                            
#objekty
Labelframe0=LabelFrame(root)
Labelframe0.place(relx=0.01,rely=0.02,relheight=0.96,relwidth=0.34)
Labelframe0.configure(text='Objects')
Labelframe0.configure(width=280)

Label1=Label(Labelframe0)
Label1.place(relx=0.04,rely=0.01,height=21,width=39)
Label1.configure(text='Show')

TCombobox1=ttk.Combobox(Labelframe0)
TCombobox1.place(relx=0.2,rely=0.01,height=25,relwidth=0.7)
TCombobox1.configure(textvariable=filtVar)
TCombobox1.configure(state='readonly')
TCombobox1['values']=('All','Visible','Above horizont','Observed','Not Observed','Visible + Not Observed') 
TCombobox1.current(0)
TCombobox1.bind('<<ComboboxSelected>>',objfilter)

Scrolledlistbox1=ScrolledListBox(Labelframe0)
Scrolledlistbox1.place(relx=0.04,rely=0.08,relheight=0.44,relwidth=0.92)
Scrolledlistbox1.configure(background='white')
Scrolledlistbox1.configure(width=10)
Scrolledlistbox1.configure(listvariable=objsVar)        
Scrolledlistbox1.bind('<<ListboxSelect>>',objselect)

Text1=ScrolledText(Labelframe0)
Text1.place(relx=0.04,rely=0.54,relheight=0.4,relwidth=0.92)
Text1.configure(background='white')
Text1.configure(width=256)
Text1.configure(wrap=WORD)

Button3_2=Button(Labelframe0)
Button3_2.place(relx=0.05,rely=0.95,height=24,width=47)
Button3_2.configure(command=AddObj)
Button3_2.configure(text='Add') 

Button2=Button(Labelframe0)
Button2.place(relx=0.35,rely=0.95,height=24,width=47)  
Button2.configure(command=EditObj)
Button2.configure(text='Edit')
Button2.configure(state=DISABLED) 

Button3=Button(Labelframe0)
Button3.place(relx=0.65,rely=0.95,height=24,width=47) 
Button3.configure(command=DelObj)
Button3.configure(text='Delete')
Button3.configure(state=DISABLED)

#pozorovania
Labelframe1=LabelFrame(root)
Labelframe1.place(relx=0.36,rely=0.02,relheight=0.96,relwidth=0.3)
Labelframe1.configure(text='Observations')
Labelframe1.configure(width=250)

Scrolledlistbox2=ScrolledListBox(Labelframe1)
Scrolledlistbox2.place(relx=0.04,rely=0.01,relheight=0.51,relwidth=0.92)
Scrolledlistbox2.configure(background='white')
Scrolledlistbox2.configure(width=10)
Scrolledlistbox2.configure(listvariable=obssVar)           
Scrolledlistbox2.bind('<<ListboxSelect>>',obsselect)

Text2=ScrolledText(Labelframe1)
Text2.place(relx=0.04,rely=0.54,relheight=0.4,relwidth=0.92)
Text2.configure(background='white')
Text2.configure(width=234)
Text2.configure(wrap=WORD) 

Button4=Button(Labelframe1)
Button4.place(relx=0.02,rely=0.95,height=24,width=47) 
Button4.configure(command=AddObs)
Button4.configure(text='Add')
Button4.configure(state=DISABLED)

Button5=Button(Labelframe1)
Button5.place(relx=0.28,rely=0.95,height=24,width=47)   
Button5.configure(command=EditObs)
Button5.configure(text='Edit')
Button5.configure(state=DISABLED)

Button6=Button(Labelframe1)
Button6.place(relx=0.53,rely=0.95,height=24,width=47)   
Button6.configure(command=DelObs)
Button6.configure(text='Delete')
Button6.configure(state=DISABLED)

Button7=Button(Labelframe1)
Button7.place(relx=0.78,rely=0.95,height=24,width=47) 
Button7.configure(command=ShowImg)
Button7.configure(state=DISABLED)
Button7.configure(text='Image')

#obrazky a datum
Label0=Label(root)
Label0.place(relx=0.68,rely=0.02,height=21,width=130)
Label0.configure(text='UTC Date&Time')

Entry1=Entry(root)
Entry1.place(relx=0.78,rely=0.02,height=25,relwidth=0.12)
Entry1.configure(background='white')
Entry1.configure(textvariable=dateVar)

Button1=Button(root)
Button1.place(relx=0.92,rely=0.02,height=24,width=55)
Button1.configure(command=NowTime)
Button1.configure(text='Now')

frame2=Frame(root)
frame2.place(relx=0.68,rely=0.08,relheight=0.44,relwidth=0.3)
canvas2=FigureCanvasTkAgg(figAlt,frame2)
canvas2.get_tk_widget().pack(side='top',fill='both',expand=1)

frame1=Frame(root)
frame1.place(relx=0.68,rely=0.54,relheight=0.44,relwidth=0.3)         
canvas1=FigureCanvasTkAgg(figObj,frame1)
canvas1.get_tk_widget().pack(side='top',fill='both',expand=1)

#menu
Popupmenu1=Menu(root,tearoff=0)
fileM= Menu(Popupmenu1,tearoff=0)    
Popupmenu1.add_cascade(menu=fileM,label='File')
fileM.add_command(command=NewFile,label='New')
fileM.add_command(command=OpenFile,label='Open')
fileM.add_command(command=SaveFile,label='Save')
fileM.add_separator()
fileM.add_command(command=Exit,label='Exit') 
import_export=Menu(Popupmenu1,tearoff=0) 
Popupmenu1.add_cascade(menu=import_export,label='Import/Export',state=DISABLED)  
Popupmenu1.add_command(command=Settings,label='Settings')
Popupmenu1.add_command(command=About,label='About')
root.config(menu=Popupmenu1)

NowTime()
objfilter()

if not os.path.isfile('data/settings.ops'):
    messagebox.showwarning('ObsPlanner','Please, configure your settings first!')
    Settings()

mainloop()
