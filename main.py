#!/usr/bin/python3
import sys
import os
import pickle
import subprocess
import shutil
import copy

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk

from PIL import ImageTk,Image

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
import objects_import

class siteClass():
    def __init__(self,name,lat,lon,ele,limits=None):
        self.name=name
        self.lat=lat
        self.lon=lon
        self.ele=ele
        if limits is None: self.limits=[0,90,0,360]     #min_alt,max_alt,min_az,max_az
        else: self.limits=limits

def sort(zoznam):
    #sorting objects -> adding "0" between letters and digits
    objSort=[]
    order={}
    for x in zoznam:
        for i in range(len(x)):
            try:
                int(x[i])
                break
            except: pass
        order[x[:i]+x[i:].rjust(10,'0')]=x
    for x in sorted(order.keys()):
        objSort.append(order[x])
    return objSort

def sortObs(zoznam):
    #sort observations by JulDate
    obsSort=[]
    order={}
    for x in zoznam: order[zoznam[x].jd]=x
    for x in sorted(order): obsSort.append(order[x])
    return obsSort

def About():
    global img
    top=tk.Toplevel()
    top.lift()
    top.geometry('310x240')
    top.title('About')
    try: top.iconbitmap('ObsPlanner.ico')   #win
    except: pass
    top.resizable(False,False)
    top.configure(background=colors['window'])

    img=Image.open('ObsPlanner.png')
    img=img.resize((80,80),Image.ANTIALIAS)
    img=ImageTk.PhotoImage(img)
    LabelImg=tk.Label(top)
    LabelImg.place(relx=0.37,rely=0.04,height=80,width=80)
    LabelImg.configure(image=img)
    LabelImg.configure(background=colors['window'])

    Label1=tk.Label(top)
    Label1.place(relx=0.0,rely=0.4,height=27,width=310)
    Label1.configure(font='-family {DejaVu Sans} -size 14 -weight bold -slant roman -underline 0 -overstrike 0')
    Label1.configure(text='ObsPlanner')
    Label1.configure(background=colors['window'])
    Label1.configure(fg=colors['text'])

    Label3=tk.Label(top)
    Label3.place(relx=0.0,rely=0.52,height=21,width=310)
    Label3.configure(text='version 0.1.5')
    Label3.configure(background=colors['window'])
    Label3.configure(fg=colors['text'])

    Label4=tk.Label(top)
    Label4.place(relx=0.0,rely=0.64,height=21,width=310)
    Label4.configure(font='-family {DejaVu Sans} -size 10 -weight normal -slant roman -underline 1 -overstrike 0')
    Label4.configure(foreground=colors['url'])
    Label4.configure(background=colors['window'])
    Label4.configure(cursor='hand2')
    Label4.configure(text='http://pavolg.6f.sk')
    Label4.bind('<Button-1>',href)

    Label4_1=tk.Label(top)
    Label4_1.place(relx=0.0,rely=0.76,height=21,width=310)
    Label4_1.configure(font='-family {DejaVu Sans} -size 10 -weight normal -slant roman -underline 1 -overstrike 0')
    Label4_1.configure(foreground=colors['url'])
    Label4_1.configure(background=colors['window'])
    Label4_1.configure(cursor='hand2')
    Label4_1.configure(text='https://github.com/pavolgaj/ObsPlanner')
    Label4_1.bind('<Button-1>',href)

    Label2=tk.Label(top)
    Label2.place(relx=0.0,rely=0.88,height=21,width=310)
    Label2.configure(text='(c) Pavol Gajdoš, 2019 - 2020')
    Label2.configure(background=colors['window'])
    Label2.configure(fg=colors['text'])

def AddObj(obj=None):
    global changed

    def save():
        global changed
        #kontrola vstupu
        if len(nameVar.get())==0:
            messagebox.showerror('Name Error','"Name" not given!')
            top.lift()
            return
        else: name=nameVar.get().strip()
        try:
            if ':' in raVar.get(): ra=stars.readDMS(raVar.get(),deg=True)
            else: ra=float(raVar.get())
        except:
            messagebox.showerror('RA Error','Wrong RA format! Correct format is "H:M:S" or "H.h" (decimal number in hours).')
            top.lift()
            return
        try:
            if ':' in decVar.get(): dec=stars.readDMS(decVar.get(),deg=True)
            else: dec=float(decVar.get())
        except:
            messagebox.showerror('DEC Error','Wrong DEC format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
            top.lift()
            return
        if len(constVar.get())==0:
            messagebox.showerror('Constelation Error','"Constelation" not given!')
            top.lift()
            return

        #nacitanie udajov a pridanie objektu
        note=TextO.get('1.0',tk.END)
        if obj is None:
            objects.add(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),typeVar.get().strip(),note.strip(),constVar.get().strip())
        else:
            if not name==obj.name:
                ans=messagebox.askquestion('Edit Object',\
                'Object name was changed. Old object (with all observations) will be deleted! Do you want to continue?',type='yesno')
                if ans=='no':
                    top.lift()
                    return
                del objects.objects[obj.name]
                objects.add(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),typeVar.get().strip(),note.strip(),\
                constVar.get().strip())
            else: objects.objects[name]['object']=stars.star(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),\
            typeVar.get().strip(),note.strip(),constVar.get().strip())

        zoznam=objfilter()
        if name not in zoznam:
            filtVar.set('All')
            zoznam=objfilter()
        fake=fakeEvt(zoznam.index(name),zoznam)
        objselect(fake)

        changed=True
        top.destroy()
        root.lift()

    def detect():
        constVar.set('')
        try:
            if ':' in raVar.get(): ra=stars.readDMS(raVar.get(),deg=True)
            else: ra=float(raVar.get())
        except:
            messagebox.showerror('RA Error','Wrong RA format! Correct format is "H:M:S" or "H.h" (decimal number in hours).')
            top.lift()
            return
        try:
            if ':' in decVar.get(): dec=stars.readDMS(decVar.get(),deg=True)
            else: dec=float(decVar.get())
        except:
            messagebox.showerror('DEC Error','Wrong DEC format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
            top.lift()
            return
        found=[]
        for const in constellations:
            if constellations[const].testPoint(ra,dec):
                found.append(const)
        if len(found)==1: constVar.set(found[0])
        elif len(found)==0:
            messagebox.showwarning('Constellation','Constellation not detected! Please, add it manually.')
            top.lift()
        else:
            messagebox.showwarning('Constellation','Multiple possible constellations detected ('+', '.join(found)+')! Please, add it manually.')
            top.lift()

    top=tk.Tk()
    top.lift()
    top.geometry('250x350')
    top.title('Object')
    try: top.iconbitmap('ObsPlanner.ico')   #win
    except: pass
    top.resizable(False,False)
    top.configure(background=colors['window'])

    nameVar=tk.StringVar(top)
    raVar=tk.StringVar(top)
    decVar=tk.StringVar(top)
    constVar=tk.StringVar(top)
    magVar=tk.StringVar(top)
    sizeVar=tk.StringVar(top)
    typeVar=tk.StringVar(top)

    if obj is not None:
        nameVar.set(obj.name)
        raVar.set(stars.printDMS(obj.ra))
        decVar.set(stars.printDMS(obj.dec))
        constVar.set(obj.const)
        magVar.set(obj.mag)
        sizeVar.set(obj.size)
        typeVar.set(obj.type)

    #objekty
    Label1=tk.Label(top)
    Label1.place(relx=0.01,rely=0.02,height=21,width=43)
    Label1.configure(text='Name')
    Label1.configure(anchor='w')
    Label1.configure(fg=colors['text'])
    Label1.configure(background=colors['window'])

    Entry1=tk.Entry(top)
    Entry1.place(relx=0.2,rely=0.02,height=25,relwidth=0.75)
    Entry1.configure(background=colors['bg'])
    Entry1.configure(fg=colors['text'])
    Entry1.configure(textvariable=nameVar)
    if colors['text']=='red':
        Entry1.configure(selectbackground=colors['select_bg'])
        Entry1.configure(selectforeground=colors['select_text'])


    Label2=tk.Label(top)
    Label2.place(relx=0.01,rely=0.10,height=21,width=43)
    Label2.configure(text='RA')
    Label2.configure(anchor='w')
    Label2.configure(fg=colors['text'])
    Label2.configure(background=colors['window'])

    Entry2=tk.Entry(top)
    Entry2.place(relx=0.2,rely=0.10,height=25,relwidth=0.75)
    Entry2.configure(background=colors['bg'])
    Entry2.configure(textvariable=raVar)
    Entry2.configure(fg=colors['text'])
    if colors['text']=='red':
        Entry2.configure(selectbackground=colors['select_bg'])
        Entry2.configure(selectforeground=colors['select_text'])

    Label3=tk.Label(top)
    Label3.place(relx=0.01,rely=0.18,height=21,width=43)
    Label3.configure(text='DEC')
    Label3.configure(anchor='w')
    Label3.configure(fg=colors['text'])
    Label3.configure(background=colors['window'])

    Entry3=tk.Entry(top)
    Entry3.place(relx=0.2,rely=0.18,height=25,relwidth=0.75)
    Entry3.configure(background=colors['bg'])
    Entry3.configure(textvariable=decVar)
    Entry3.configure(fg=colors['text'])
    if colors['text']=='red':
        Entry3.configure(selectbackground=colors['select_bg'])
        Entry3.configure(selectforeground=colors['select_text'])

    Label8=tk.Label(top)
    Label8.place(relx=0.01,rely=0.26,height=21,width=90)
    Label8.configure(text='Constellation')
    Label8.configure(anchor='w')
    Label8.configure(fg=colors['text'])
    Label8.configure(background=colors['window'])

    Entry7=tk.Entry(top)
    Entry7.place(relx=0.4,rely=0.26,height=25,relwidth=0.35)
    Entry7.configure(background=colors['bg'])
    Entry7.configure(textvariable=constVar)
    if colors['text']=='red':
        Entry7.configure(selectbackground=colors['select_bg'])
        Entry7.configure(selectforeground=colors['select_text'])
    Entry7.configure(fg=colors['text'])

    Button2=tk.Button(top)
    Button2.place(relx=0.76,rely=0.26,height=24,width=47)
    Button2.configure(text='Detect')
    Button2.configure(command=detect)
    Button2.configure(fg=colors['text'])
    Button2.configure(background=colors['window'])

    Label4=tk.Label(top)
    Label4.place(relx=0.01,rely=0.34,height=21,width=43)
    Label4.configure(text='Mag')
    Label4.configure(anchor='w')
    Label4.configure(fg=colors['text'])
    Label4.configure(background=colors['window'])

    Entry4=tk.Entry(top)
    Entry4.place(relx=0.2,rely=0.34,height=25,relwidth=0.75)
    Entry4.configure(background=colors['bg'])
    Entry4.configure(fg=colors['text'])
    if colors['text']=='red':
        Entry4.configure(selectbackground=colors['select_bg'])
        Entry4.configure(selectforeground=colors['select_text'])
    Entry4.configure(textvariable=magVar)

    Label5=tk.Label(top)
    Label5.place(relx=0.01,rely=0.42,height=21,width=43)
    Label5.configure(text='Size')
    Label5.configure(anchor='w')
    Label5.configure(fg=colors['text'])
    Label5.configure(background=colors['window'])

    Entry5=tk.Entry(top)
    Entry5.place(relx=0.2,rely=0.42,height=25,relwidth=0.75)
    Entry5.configure(background=colors['bg'])
    Entry5.configure(fg=colors['text'])
    if colors['text']=='red':
        Entry5.configure(selectbackground=colors['select_bg'])
        Entry5.configure(selectforeground=colors['select_text'])
    Entry5.configure(textvariable=sizeVar)

    Label6=tk.Label(top)
    Label6.place(relx=0.01,rely=0.50,height=21,width=43)
    Label6.configure(text='Type')
    Label6.configure(anchor='w')
    Label6.configure(fg=colors['text'])
    Label6.configure(background=colors['window'])

    Entry6=tk.Entry(top)
    Entry6.place(relx=0.2,rely=0.50,height=25,relwidth=0.75)
    Entry6.configure(background=colors['bg'])
    Entry6.configure(fg=colors['text'])
    if colors['text']=='red':
        Entry6.configure(selectbackground=colors['select_bg'])
        Entry6.configure(selectforeground=colors['select_text'])
    Entry6.configure(textvariable=typeVar)

    Label7=tk.Label(top)
    Label7.place(relx=0.01,rely=0.58,height=21,width=43)
    Label7.configure(text='Notes')
    Label7.configure(anchor='w')
    Label7.configure(fg=colors['text'])
    Label7.configure(background=colors['window'])

    TextO=ScrolledText(top)
    TextO.place(relx=0.2,rely=0.58,relheight=0.33,relwidth=0.75)
    TextO.configure(background=colors['bg'])
    TextO.configure(fg=colors['text'])
    if colors['text']=='red':
        TextO.configure(selectbackground=colors['select_bg'])
        TextO.configure(selectforeground=colors['select_text'])
        TextO.configure(inactiveselectbackground=colors['select_bg'])
    TextO.configure(width=10)
    TextO.configure(wrap=tk.WORD)

    if obj is not None:
        #vypis info o objekte
        old=sys.stdout
        #redirect output to text field
        sys.stdout=StdoutRedirector(TextO)
        print(obj.note)
        sys.stdout=old

    Button1=tk.Button(top)
    Button1.place(relx=0.45,rely=0.93,height=24,width=47)
    Button1.configure(text='Save')
    Button1.configure(command=save)
    Button1.configure(background=colors['window'])
    Button1.configure(fg=colors['text'])


def AddObs(obs=None):
    global changed
    def addObserver(obs=None):
        def saveObs():
            if obs is not None: settings['observers'].remove(obs)
            settings['observers'].append(obsNameVar.get())
            TCombobox1['values']=sorted(settings['observers'])
            TCombobox1.current(sorted(settings['observers']).index(obsNameVar.get()))
            topObs.destroy()
            top.lift()

        topObs=tk.Tk()
        topObs.lift()
        topObs.geometry('300x80')
        topObs.title('Observer')
        try: topObs.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        topObs.resizable(False,False)

        obsNameVar=tk.StringVar(topObs)

        if obs is not None: obsNameVar.set(obs)

        Label1=tk.Label(topObs)
        Label1.place(relx=0.01,rely=0.1,height=21,width=43)
        Label1.configure(text='Name')

        Entry1=tk.Entry(topObs)
        Entry1.place(relx=0.2,rely=0.1,height=25,relwidth=0.75)
        Entry1.configure(background=colors['bg'])
        Entry1.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry1.configure(selectbackground=colors['select_bg'])
            Entry1.configure(selectforeground=colors['select_text'])
        Entry1.configure(textvariable=obsNameVar)

        Button1=tk.Button(topObs)
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
                topSite.lift()

            topLims=tk.Tk()
            topLims.lift()
            topLims.geometry('400x150')
            topLims.title('Limits')
            try: topLims.iconbitmap('ObsPlanner.ico')   #win
            except: pass
            topLims.resizable(False,False)

            minAltVar=tk.DoubleVar(topLims)
            maxAltVar=tk.DoubleVar(topLims)
            minAzmVar=tk.DoubleVar(topLims)
            maxAzmVar=tk.DoubleVar(topLims)

            if site is not None: limits=settings['sites'][site].limits
            else: limits=new_limits

            minAltVar.set(limits[0])
            maxAltVar.set(limits[1])
            minAzmVar.set(limits[2])
            maxAzmVar.set(limits[3])

            Label1=tk.Label(topLims)
            Label1.place(relx=0.25,rely=0.05,height=21,width=43)
            Label1.configure(text='Min')
            Label1.configure(anchor='w')

            Label2=tk.Label(topLims)
            Label2.place(relx=0.62,rely=0.05,height=21,width=43)
            Label2.configure(text='Max')
            Label2.configure(anchor='w')

            Label3=tk.Label(topLims)
            Label3.place(relx=0.05,rely=0.25,height=21,width=80 )
            Label3.configure(text='Altitude')
            Label3.configure(anchor='w')

            Entry1=tk.Entry(topLims)
            Entry1.place(relx=0.25,rely=0.25,height=25,relwidth=0.35)
            Entry1.configure(background=colors['bg'])
            Entry1.configure(fg=colors['text'])
            if colors['text']=='red':
                Entry1.configure(selectbackground=colors['select_bg'])
                Entry1.configure(selectforeground=colors['select_text'])
            Entry1.configure(textvariable=minAltVar)

            Entry2=tk.Entry(topLims)
            Entry2.place(relx=0.62,rely=0.25,height=25,relwidth=0.35)
            Entry2.configure(background=colors['bg'])
            Entry2.configure(fg=colors['text'])
            if colors['text']=='red':
                Entry2.configure(selectbackground=colors['select_bg'])
                Entry2.configure(selectforeground=colors['select_text'])
            Entry2.configure(textvariable=maxAltVar)

            Label4=tk.Label(topLims)
            Label4.place(relx=0.05,rely=0.45,height=21,width=80)
            Label4.configure(text='Azimut')
            Label4.configure(anchor='w')

            Entry3=tk.Entry(topLims)
            Entry3.place(relx=0.25,rely=0.45,height=25,relwidth=0.35)
            Entry3.configure(background=colors['bg'])
            Entry3.configure(fg=colors['text'])
            if colors['text']=='red':
                Entry3.configure(selectbackground=colors['select_bg'])
                Entry3.configure(selectforeground=colors['select_text'])
            Entry3.configure(textvariable=minAzmVar)

            Entry4=tk.Entry(topLims)
            Entry4.place(relx=0.62,rely=0.45,height=25,relwidth=0.35)
            Entry4.configure(background=colors['bg'])
            Entry4.configure(fg=colors['text'])
            if colors['text']=='red':
                Entry4.configure(selectbackground=colors['select_bg'])
                Entry4.configure(selectforeground=colors['select_text'])
            Entry4.configure(textvariable=maxAzmVar)

            Button2=tk.Button(topLims)
            Button2.place(relx=0.45,rely=0.7,height=29,width=58)
            Button2.configure(text='Save')
            Button2.configure(command=saveLims)

        def saveSite():
            try:
                if ':' in siteLatVar.get(): lat=stars.readDMS(siteLatVar.get(),deg=True)
                else: lat=float(siteLatVar.get())
            except:
                messagebox.showerror('Latitude Error','Wrong Latitude format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
                topSite.lift()
                return
            try:
                if ':' in siteLonVar.get(): lon=stars.readDMS(siteLonVar.get(),deg=True)
                else: lon=float(siteLonVar.get())
            except:
                messagebox.showerror('Longitude Error','Wrong Longitude format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
                topSite.lift()
                return
            if site is not None: del settings['sites'][site]
            settings['sites'][siteNameVar.get()]=siteClass(siteNameVar.get(),lat,lon,float(siteEleVar.get()),limits)
            TCombobox2['values']=sorted(settings['sites'].keys())
            TCombobox2.current(sorted(settings['sites'].keys()).index(siteNameVar.get()))
            topSite.destroy()
            top.lift()

        topSite=tk.Tk()
        topSite.lift()
        topSite.geometry('230x200')
        topSite.title('Site')
        try: topSite.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        topSite.resizable(False,False)

        siteNameVar=tk.StringVar(topSite)
        siteLatVar=tk.StringVar(topSite)
        siteLonVar=tk.StringVar(topSite)
        siteEleVar=tk.StringVar(topSite)
        new_limits=[0,90,0,360]
        limits=new_limits

        if site is not None:
            siteNameVar.set(site)
            siteLatVar.set(stars.printDMS(settings['sites'][site].lat))
            siteLonVar.set(stars.printDMS(settings['sites'][site].lon))
            siteEleVar.set(settings['sites'][site].ele)
            limits=settings['sites'][site].limits

        Label1=tk.Label(topSite)
        Label1.place(relx=0.05,rely=0.05,height=21,width=43)
        Label1.configure(text='Name')
        Label1.configure(anchor='w')

        Entry1=tk.Entry(topSite)
        Entry1.place(relx=0.35,rely=0.05,height=25,relwidth=0.6)
        Entry1.configure(background=colors['bg'])
        Entry1.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry1.configure(selectbackground=colors['select_bg'])
            Entry1.configure(selectforeground=colors['select_text'])
        Entry1.configure(textvariable=siteNameVar)

        Label2=tk.Label(topSite)
        Label2.place(relx=0.05,rely=0.25,height=21,width=57)
        Label2.configure(text='Latitude')
        Label2.configure(anchor='w')

        Entry2=tk.Entry(topSite)
        Entry2.place(relx=0.35,rely=0.25,height=25,relwidth=0.6)
        Entry2.configure(background=colors['bg'])
        Entry2.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry2.configure(selectbackground=colors['select_bg'])
            Entry2.configure(selectforeground=colors['select_text'])
        Entry2.configure(textvariable=siteLatVar)

        Label3=tk.Label(topSite)
        Label3.place(relx=0.05,rely=0.45,height=21,width=68)
        Label3.configure(text='Longitude')
        Label3.configure(anchor='w')

        Entry3=tk.Entry(topSite)
        Entry3.place(relx=0.35,rely=0.45,height=25,relwidth=0.6)
        Entry3.configure(background=colors['bg'])
        Entry3.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry3.configure(selectbackground=colors['select_bg'])
            Entry3.configure(selectforeground=colors['select_text'])
        Entry3.configure(textvariable=siteLonVar)

        Label4=tk.Label(topSite)
        Label4.place(relx=0.05,rely=0.65,height=21,width=65)
        Label4.configure(text='Elevation')
        Label4.configure(anchor='w')

        Entry4=tk.Entry(topSite)
        Entry4.place(relx=0.35,rely=0.65,height=25,relwidth=0.6)
        Entry4.configure(background=colors['bg'])
        Entry4.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry4.configure(selectbackground=colors['select_bg'])
            Entry4.configure(selectforeground=colors['select_text'])
        Entry4.configure(textvariable=siteEleVar)

        Button1=tk.Button(topSite)
        Button1.place(relx=0.2,rely=0.82,height=29,width=58)
        Button1.configure(text='Limits')
        Button1.configure(command=setLimits)

        Button2=tk.Button(topSite)
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
            top.lift()

        topTel=tk.Tk()
        topTel.lift()
        topTel.geometry('400x80')
        topTel.title('Telescope')
        try: topTel.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        topTel.resizable(False,False)

        telNameVar=tk.StringVar(topTel)

        if tel is not None: telNameVar.set(tel)

        Label1=tk.Label(topTel)
        Label1.place(relx=0.01,rely=0.1,height=21,width=43)
        Label1.configure(text='Name')

        Entry1=tk.Entry(topTel)
        Entry1.place(relx=0.15,rely=0.1,height=25,relwidth=0.82)
        Entry1.configure(background=colors['bg'])
        Entry1.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry1.configure(selectbackground=colors['select_bg'])
            Entry1.configure(selectforeground=colors['select_text'])
        Entry1.configure(textvariable=telNameVar)

        Button1=tk.Button(topTel)
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
                topObj.lift()
                return
            else: name=nameVar.get().strip()
            try:
                if ':' in raVar.get(): ra=stars.readDMS(raVar.get(),deg=True)
                else: ra=float(raVar.get())
            except:
                messagebox.showerror('RA Error','Wrong RA format! Correct format is "H:M:S" or "H.h" (decimal number in hours).')
                topObj.lift()
                return
            try:
                if ':' in decVar.get(): dec=stars.readDMS(decVar.get(),deg=True)
                else: dec=float(decVar.get())
            except:
                messagebox.showerror('DEC Error','Wrong DEC format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
                topObj.lift()
                return
            if len(constVar.get())==0:
                messagebox.showerror('Constelation Error','"Constelation" not given!')
                topObj.lift()
                return

            #nacitanie udajov a pridanie objektu
            note=TextO.get('1.0',tk.END)
            if obj is None:
                objects.add(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),typeVar.get().strip(),note.strip(),constVar.get().strip())
            else:
                if not name==obj.name:
                    ans=messagebox.askquestion('Edit Object',\
                    'Object name was changed. Old object (with all observations) will be deleted! Do you want to continue?',type='yesno')
                    if ans=='no':
                        topObj.lift()
                        return
                    del objects.objects[obj.name]
                    objects.add(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),typeVar.get().strip(),note.strip(),\
                    constVar.get().strip())
                else: objects.objects[name]['object']=stars.star(name,ra,dec,magVar.get().strip(),sizeVar.get().strip(),\
                typeVar.get().strip(),note.strip(),constVar.get().strip())
            zoznam=objfilter()
            if name not in zoznam:
                filtVar.set('All')
                zoznam=objfilter()
            fake=fakeEvt(zoznam.index(name),zoznam)
            objselect(fake)

            TCombobox4['values']=sort(objects.objects.keys())
            TCombobox4.current(sort(objects.objects.keys()).index(objZ.name))

            topObj.destroy()
            top.lift()

        def detect():
            constVar.set('')
            try:
                if ':' in raVar.get(): ra=stars.readDMS(raVar.get(),deg=True)
                else: ra=float(raVar.get())
            except:
                messagebox.showerror('RA Error','Wrong RA format! Correct format is "H:M:S" or "H.h" (decimal number in hours).')
                topObj.lift()
                return
            try:
                if ':' in decVar.get(): dec=stars.readDMS(decVar.get(),deg=True)
                else: dec=float(decVar.get())
            except:
                messagebox.showerror('DEC Error','Wrong DEC format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
                topObj.lift()
                return
            for const in constellations:
                if constellations[const].testPoint(ra,dec):
                    constVar.set(const)
                    return

        topObj=tk.Tk()
        topObj.lift()
        topObj.geometry('250x350')
        topObj.title('Object')
        try: topObj.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        topObj.resizable(False,False)

        nameVar=tk.StringVar(topObj)
        raVar=tk.StringVar(topObj)
        decVar=tk.StringVar(topObj)
        constVar=tk.StringVar(topObj)
        magVar=tk.StringVar(topObj)
        sizeVar=tk.StringVar(topObj)
        typeVar=tk.StringVar(topObj)

        if obj is not None:
            nameVar.set(obj.name)
            raVar.set(stars.printDMS(obj.ra))
            decVar.set(stars.printDMS(obj.dec))
            constVar.set(obj.const)
            magVar.set(obj.mag)
            sizeVar.set(obj.size)
            typeVar.set(obj.type)

        #objekty
        Label1=tk.Label(topObj)
        Label1.place(relx=0.01,rely=0.02,height=21,width=43)
        Label1.configure(text='Name')
        Label1.configure(anchor='w')

        Entry1=tk.Entry(topObj)
        Entry1.place(relx=0.2,rely=0.02,height=25,relwidth=0.75)
        Entry1.configure(background=colors['bg'])
        Entry1.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry1.configure(selectbackground=colors['select_bg'])
            Entry1.configure(selectforeground=colors['select_text'])
        Entry1.configure(textvariable=nameVar)

        Label2=tk.Label(topObj)
        Label2.place(relx=0.01,rely=0.10,height=21,width=43)
        Label2.configure(text='RA')
        Label2.configure(anchor='w')

        Entry2=tk.Entry(topObj)
        Entry2.place(relx=0.2,rely=0.10,height=25,relwidth=0.75)
        Entry2.configure(background=colors['bg'])
        Entry2.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry2.configure(selectbackground=colors['select_bg'])
            Entry2.configure(selectforeground=colors['select_text'])
        Entry2.configure(textvariable=raVar)

        Label3=tk.Label(topObj)
        Label3.place(relx=0.01,rely=0.18,height=21,width=43)
        Label3.configure(text='DEC')
        Label3.configure(anchor='w')

        Entry3=tk.Entry(topObj)
        Entry3.place(relx=0.2,rely=0.18,height=25,relwidth=0.75)
        Entry3.configure(background=colors['bg'])
        Entry3.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry3.configure(selectbackground=colors['select_bg'])
            Entry3.configure(selectforeground=colors['select_text'])
        Entry3.configure(textvariable=decVar)

        Label8=tk.Label(topObj)
        Label8.place(relx=0.01,rely=0.26,height=21,width=90)
        Label8.configure(text='Constellation')
        Label8.configure(anchor='w')

        Entry7=tk.Entry(topObj)
        Entry7.place(relx=0.4,rely=0.26,height=25,relwidth=0.35)
        Entry7.configure(background=colors['bg'])
        Entry7.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry7.configure(selectbackground=colors['select_bg'])
            Entry7.configure(selectforeground=colors['select_text'])
        Entry7.configure(textvariable=constVar)

        Button2=tk.Button(topObj)
        Button2.place(relx=0.76,rely=0.26,height=24,width=47)
        Button2.configure(text='Detect')
        Button2.configure(command=detect)

        Label4=tk.Label(topObj)
        Label4.place(relx=0.01,rely=0.34,height=21,width=43)
        Label4.configure(text='Mag')
        Label4.configure(anchor='w')

        Entry4=tk.Entry(topObj)
        Entry4.place(relx=0.2,rely=0.34,height=25,relwidth=0.75)
        Entry4.configure(background=colors['bg'])
        Entry4.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry4.configure(selectbackground=colors['select_bg'])
            Entry4.configure(selectforeground=colors['select_text'])
        Entry4.configure(textvariable=magVar)

        Label5=tk.Label(topObj)
        Label5.place(relx=0.01,rely=0.42,height=21,width=43)
        Label5.configure(text='Size')
        Label5.configure(anchor='w')

        Entry5=tk.Entry(topObj)
        Entry5.place(relx=0.2,rely=0.42,height=25,relwidth=0.75)
        Entry5.configure(background=colors['bg'])
        Entry5.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry5.configure(selectbackground=colors['select_bg'])
            Entry5.configure(selectforeground=colors['select_text'])
        Entry5.configure(textvariable=sizeVar)

        Label6=tk.Label(topObj)
        Label6.place(relx=0.01,rely=0.50,height=21,width=43)
        Label6.configure(text='Type')
        Label6.configure(anchor='w')

        Entry6=tk.Entry(topObj)
        Entry6.place(relx=0.2,rely=0.50,height=25,relwidth=0.75)
        Entry6.configure(background=colors['bg'])
        Entry6.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry6.configure(selectbackground=colors['select_bg'])
            Entry6.configure(selectforeground=colors['select_text'])
        Entry6.configure(textvariable=typeVar)

        Label7=tk.Label(topObj)
        Label7.place(relx=0.01,rely=0.58,height=21,width=43)
        Label7.configure(text='Notes')
        Label7.configure(anchor='w')

        TextO=ScrolledText(topObj)
        TextO.place(relx=0.2,rely=0.58,relheight=0.33,relwidth=0.75)
        TextO.configure(background=colors['bg'])
        TextO.configure(fg=colors['text'])
        if colors['text']=='red':
            TextO.configure(selectbackground=colors['select_bg'])
            TextO.configure(selectforeground=colors['select_text'])
        TextO.configure(width=10)
        TextO.configure(wrap=tk.WORD)

        if obj is not None:
            #vypis info o objekte
            old=sys.stdout
            #redirect output to text field
            sys.stdout=StdoutRedirector(TextO)
            print(obj.note)
            sys.stdout=old

        Button1=tk.Button(topObj)
        Button1.place(relx=0.45,rely=0.93,height=24,width=47)
        Button1.configure(text='Save')
        Button1.configure(command=save)



    def edObsObj():
        addObsObj(objects.objects[objVar.get()]['object'])

    def addImgObs(img=None):
        filetypes=[('JPG Images','*.jpg;*.jpeg'),('TIFF Images','*.tiff'),('PNG Images','*.png'),('FITS Images','*.fit;*.fits;*.fts'),\
        ('BMP Images','*.bmp'),('XISF Images','*.xisf'),('All files','*.*')]
        if img is None:
            name0=filedialog.askopenfilename(parent=top,filetypes=filetypes,title='Observation - Image',defaultextension='.jpg')
        else:
            name0=filedialog.askopenfilename(parent=top,filetypes=filetypes,title='Observation - Image',defaultextension='.jpg',\
            initialdir=img[:img.rfind('/')],initialfile=img[img.rfind('/')+1:])
        if len(name0)>0:
            name0=name0.replace('\\','/')
            cwd=os.getcwd().replace('\\','/')+'/'
            if cwd in name0: name0=name0.replace(cwd,'')    #uloz relativnu cestu
            imgVar.set(name0)

    def edImgObs():
        addImgObs(imgVar.get())


    def saveObs():
        global changed
        note=TextO.get('1.0',tk.END)
        try: dt=datetime.datetime.strptime(obsDateVar.get(),'%Y-%m-%d %H:%M:%S')
        except:
            messagebox.showerror('Date/Time Error','Wrong date/time format! Correct format is "Y-m-d H:M:S". Date/time set to current time.')
            top.lift()
            return
        if obs is not None: del objects.objects[obs.obj]['obs'][obs.date]

        path=imgVar.get().strip()
        if len(path)>0:
            if not os.path.isfile(path):
                messagebox.showerror('ObsPlanner','Image "'+path+'" not found!')
                top.lift()
                return
            if settings['file_copy'] and len(path)>0:
                #zkopiruj do images
                path1='images/'+objVar.get().replace(' ','_')+'_'+obsDateVar.get().replace(' ','_').replace(':','-')+path[path.find('.'):]
                if not (path==path1): shutil.copy2(path,path1)
                path=path1

        objects.addObs(objVar.get(),dt,observerVar.get(),telVar.get(),settings['sites'][siteVar.get()],image=path,note=note.strip())

        zoznam=objfilter()
        if not objVar.get() in zoznam:
            filtVar.set('All')
            zoznam=objfilter()
        fake=fakeEvt(zoznam.index(objVar.get()),zoznam)
        objselect(fake)

        zoznam=sortObs(obsZ)
        fake=fakeEvt(zoznam.index(obsDateVar.get()),zoznam)
        obsselect(fake)

        import_export.entryconfig('Export All Observations',state='normal')
        changed=True
        top.destroy()
        root.lift()

    top=tk.Tk()
    top.lift()
    top.geometry('450x400')
    top.title('Observation')
    try: top.iconbitmap('ObsPlanner.ico')   #win
    except: pass
    top.resizable(False,False)

    observerVar=tk.StringVar(top)
    siteVar=tk.StringVar(top)
    telVar=tk.StringVar(top)
    objVar=tk.StringVar(top)
    obsDateVar=tk.StringVar(top)
    imgVar=tk.StringVar(top)

    obsDateVar.set(dateVar.get())

    Label1=tk.Label(top)
    Label1.place(relx=0.02,rely=0.02,height=21,width=63)
    Label1.configure(text='Observer')
    Label1.configure(anchor='w')

    if colors['text']=='red':
        top.option_add('*TCombobox*Listbox*Background',colors['bg'])
        top.option_add('*TCombobox*Listbox*Foreground',colors['text'])
    style=ttk.Style(top)
    style.map('TCombobox',selectbackground=[('readonly',colors['bg'])])
    style.map('TCombobox',fieldbackground=[('readonly',colors['bg'])])
    style.map('TCombobox',foreground=[('readonly',colors['text'])])
    style.map('TCombobox',selectforeground=[('readonly',colors['text'])])

    TCombobox1=ttk.Combobox(top)
    TCombobox1.place(relx=0.27,rely=0.02,height=25,relwidth=0.45)
    TCombobox1.configure(textvariable=observerVar)
    TCombobox1.configure(takefocus='')
    TCombobox1.configure(state='readonly')
    if len(settings['observers'])>0:
        TCombobox1['values']=sorted(settings['observers'])
        TCombobox1.current(sorted(settings['observers']).index(settings['default_obs']))

    ButtonOA=tk.Button(top)
    ButtonOA.place(relx=0.75,rely=0.02,height=24,width=43)
    ButtonOA.configure(text='Add')
    ButtonOA.configure(command=addObserver)

    ButtonOE=tk.Button(top)
    ButtonOE.place(relx=0.88,rely=0.02,height=24,width=43)
    ButtonOE.configure(text='Edit')
    ButtonOE.configure(command=editObserver)

    Label2=tk.Label(top)
    Label2.place(relx=0.02,rely=0.10,height=21,width=130)
    Label2.configure(text='UTC Date/Time')
    Label2.configure(anchor='w')

    Entry1=tk.Entry(top)
    Entry1.place(relx=0.27,rely=0.10,height=25,relwidth=0.45)
    Entry1.configure(background=colors['bg'])
    Entry1.configure(fg=colors['text'])
    if colors['text']=='red':
        Entry1.configure(selectbackground=colors['select_bg'])
        Entry1.configure(selectforeground=colors['select_text'])
    Entry1.configure(textvariable=obsDateVar)

    Label3=tk.Label(top)
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

    ButtonOA=tk.Button(top)
    ButtonOA.place(relx=0.75,rely=0.18,height=25,width=43)
    ButtonOA.configure(text='Add')
    ButtonOA.configure(command=addSite)

    ButtonOE=tk.Button(top)
    ButtonOE.place(relx=0.88,rely=0.18,height=25,width=43)
    ButtonOE.configure(text='Edit')
    ButtonOE.configure(command=editSite)

    Label4=tk.Label(top)
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

    ButtonOA=tk.Button(top)
    ButtonOA.place(relx=0.75,rely=0.26,height=25,width=43)
    ButtonOA.configure(text='Add')
    ButtonOA.configure(command=addTel)

    ButtonOE=tk.Button(top)
    ButtonOE.place(relx=0.88,rely=0.26,height=25,width=43)
    ButtonOE.configure(text='Edit')
    ButtonOE.configure(command=editTel)

    Label5=tk.Label(top)
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

    ButtonObA=tk.Button(top)
    ButtonObA.place(relx=0.75,rely=0.34,height=25,width=43)
    ButtonObA.configure(text='Add')
    ButtonObA.configure(command=addObsObj)

    ButtonObE=tk.Button(top)
    ButtonObE.place(relx=0.88,rely=0.34,height=25,width=43)
    ButtonObE.configure(text='Edit')
    ButtonObE.configure(command=edObsObj)

    Label6=tk.Label(top)
    Label6.place(relx=0.02,rely=0.42,height=21,width=45)
    Label6.configure(text='Image')
    Label6.configure(anchor='w')

    Entry2=tk.Entry(top)
    Entry2.place(relx=0.27,rely=0.42,height=25,relwidth=0.45)
    Entry2.configure(background=colors['bg'])
    Entry2.configure(fg=colors['text'])
    if colors['text']=='red':
        Entry2.configure(selectbackground=colors['select_bg'])
        Entry2.configure(selectforeground=colors['select_text'])
    Entry2.configure(textvariable=imgVar)

    Button1=tk.Button(top)
    Button1.place(relx=0.75,rely=0.42,height=25,width=43)
    Button1.configure(text='Add')
    Button1.configure(command=addImgObs)

    Button1_2=tk.Button(top)
    Button1_2.place(relx=0.88,rely=0.42,height=25,width=43)
    Button1_2.configure(text='Edit')
    Button1_2.configure(command=edImgObs)

    Label7=tk.Label(top)
    Label7.place(relx=0.02,rely=0.5,height=21,width=46)
    Label7.configure(text='Note')
    Label7.configure(anchor='w')

    TextO=ScrolledText(top)
    TextO.place(relx=0.27,rely=0.5,relheight=0.35,relwidth=0.45)
    TextO.configure(background=colors['bg'])
    TextO.configure(fg=colors['text'])
    if colors['text']=='red':
        TextO.configure(selectbackground=colors['select_bg'])
        TextO.configure(selectforeground=colors['select_text'])
    TextO.configure(width=10)
    TextO.configure(wrap=tk.WORD)

    Button2=tk.Button(top)
    Button2.place(relx=0.38,rely=0.88,height=29,width=57)
    Button2.configure(text='Save')
    Button2.configure(command=saveObs)

    if obs is not None:
        observerVar.set(obs.observer)
        siteVar.set(obs.site.name)
        telVar.set(obs.telescope)
        objVar.set(obs.obj)
        obsDateVar.set(obs.date)
        imgVar.set(obs.image)

        #vypis info o objekte
        old=sys.stdout
        #redirect output to text field
        sys.stdout=StdoutRedirector(TextO)
        print(obs.note)
        sys.stdout=old


def DelObj():
    ans=messagebox.askquestion('Delete Object','Selected object (with all observations) will be deleted! Do you want to continue?',type='yesno')
    if ans=='no': return
    del objects.objects[objZ.name]
    clear()

def DelObs():
    global changed
    ans=messagebox.askquestion('Delete Observation','Selected observation will be deleted! Do you want to continue?',type='yesno')
    if ans=='no': return
    del objects.objects[objZ.name]['obs'][obsZ1.date]
    changed=True
    obsZ=objects.objects[objZ.name]['obs']

    Text2.delete(1.0,tk.END)
    obssVar.set(sortObs(obsZ))
    Button5.configure(state=tk.DISABLED)
    Button6.configure(state=tk.DISABLED)

    if len(obsZ)>0:
        import_export.entryconfig('Export Observations of Object',state='normal')
        import_export.entryconfig('Export All Observations',state='normal')
    else:
        import_export.entryconfig('Export Observations of Object',state='disabled')
        obsFound=False
        for o in objects.objects:
            if len(objects.objects[o]['obs'])>0:
                obsFound=True
                break
        if obsFound: import_export.entryconfig('Export All Observations',state='normal')
        else: import_export.entryconfig('Export All Observations',state='disabled')

def EditObj():
    AddObj(objZ)

def EditObs():
    AddObs(obsZ1)

def Exit(event=None):
    global root
    if saveQuestion()==0: return  #zrusene
    if not noSett:
        #testovanie zmeny nastaveni
        changedSet=False
        for x in settings:
            if x=='sites':
                if not len(settings['sites'])==len(settings0['sites']):
                    changedSet=True
                    break
                for y in settings['sites']:
                    if not (y in settings0['sites']):
                        changedSet=True
                        break
                    if (not settings['sites'][y].lat==settings0['sites'][y].lat) or (not settings['sites'][y].lon==settings0['sites'][y].lon)\
                     or (not settings['sites'][y].ele==settings0['sites'][y].ele) or (not settings['sites'][y].limits==settings0['sites'][y].limits):
                        changedSet=True
                        break
                if changedSet: break
            elif x=='default_site':
                if not settings['default_site'].name==settings0['default_site'].name:
                    changedSet=True
                    break
            elif x not in settings0:
                changedSet=True
                break
            else:
                if not (settings[x]==settings0[x]):
                    changedSet=True
                    break
        if changedSet:
            f=open('data/settings.ops','wb')
            pickle.dump(settings,f)
            f.close()
    root.destroy()
    root=None
    matplotlib.pyplot.close()

def NewFile(event=None):
    global changed
    global objects
    if saveQuestion()==0: return  #zrusene
    objects=objClass.objects(constellations)
    clear()
    settings['file']=''
    changed=False
    import_export.entryconfig('Export Selected Objects',state='disabled')
    import_export.entryconfig('Export Observations of Object',state='disabled')
    import_export.entryconfig('Export All Observations',state='disabled')

def NowTime():
    dt=datetime.datetime.now(datetime.timezone.utc)
    dateVar.set(dt.strftime('%Y-%m-%d %H:%M:%S'))

def OpenFile(event=None):
    global changed
    global objects
    if saveQuestion()==0: return  #zrusene

    name=filedialog.askopenfilename(parent=root,filetypes=[('ObsPlanner files','*.opd'),('All files','*.*')],title='Open file')
    name=name.replace('\\','/')

    if len(name)>0:
        objects=objClass.objects(constellations)
        objects.load(name)
        clear()
        cwd=os.getcwd().replace('\\','/')+'/'
        if cwd in name: name=name.replace(cwd,'')    #uloz relativnu cestu
        settings['file']=name
        changed=False

        obsFound=False
        for o in objects.objects:
            if len(objects.objects[o]['obs'])>0:
                obsFound=True
                break
        if obsFound: import_export.entryconfig('Export All Observations',state='normal')
        else: import_export.entryconfig('Export All Observations',state='disabled')

def SaveFile(event=None):
    global changed
    if len(settings['file'])>0:
        objects.save(settings['file'])
        changed=False
    else: SaveAsFile()

def SaveAsFile():
    global changed
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('ObsPlanner files','*.opd'),('All files','*.*')],title='Save file',defaultextension='.opd')
    name=name.replace('\\','/')
    if len(name)>0:
        objects.save(name)
        cwd=os.getcwd().replace('\\','/')+'/'
        if cwd in name: name=name.replace(cwd,'')    #uloz relativnu cestu
        settings['file']=name
        changed=False

def Settings():
    global settings,noSett,changed

    def addObserver(obs=None):
        def saveObs():
            if obs is not None: settings1['observers'].remove(obs)
            settings1['observers'].append(obsNameVar.get())
            TCombobox1['values']=sorted(settings1['observers'])
            TCombobox1.current(sorted(settings1['observers']).index(obsNameVar.get()))
            Button1_1.configure(state=tk.NORMAL)
            Button1_2.configure(state=tk.NORMAL)
            topObs.destroy()
            top.lift()

        topObs=tk.Tk()
        topObs.lift()
        topObs.geometry('300x80')
        topObs.title('Observer')
        try: topObs.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        topObs.resizable(False,False)

        obsNameVar=tk.StringVar(topObs)

        if obs is not None: obsNameVar.set(obs)

        Label1=tk.Label(topObs)
        Label1.place(relx=0.01,rely=0.1,height=21,width=43)
        Label1.configure(text='Name')

        Entry1=tk.Entry(topObs)
        Entry1.place(relx=0.2,rely=0.1,height=25,relwidth=0.75)
        Entry1.configure(background=colors['bg'])
        Entry1.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry1.configure(selectbackground=colors['select_bg'])
            Entry1.configure(selectforeground=colors['select_text'])
        Entry1.configure(textvariable=obsNameVar)

        Button1=tk.Button(topObs)
        Button1.place(relx=0.4,rely=0.6,height=24,width=60)
        Button1.configure(text='Save')
        Button1.configure(command=saveObs)

    def editObserver():
        addObserver(observerVar.get())

    def delObserver():
        settings1['observers'].remove(observerVar.get())
        TCombobox1['values']=sorted(settings1['observers'])
        if len(TCombobox1['values'])==0:
            Button1_1.configure(state=tk.DISABLED)
            Button1_2.configure(state=tk.DISABLED)
            TCombobox1.set('')
        else: TCombobox1.current(0)

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
                topSite.lift()

            topLims=tk.Tk()
            topLims.lift()
            topLims.geometry('400x150')
            topLims.title('Limits')
            topLims.resizable(False,False)
            try: topLims.iconbitmap('ObsPlanner.ico')   #win
            except: pass

            minAltVar=tk.DoubleVar(topLims)
            maxAltVar=tk.DoubleVar(topLims)
            minAzmVar=tk.DoubleVar(topLims)
            maxAzmVar=tk.DoubleVar(topLims)

            if site is not None: limits=settings1['sites'][site].limits
            else: limits=new_limits

            minAltVar.set(limits[0])
            maxAltVar.set(limits[1])
            minAzmVar.set(limits[2])
            maxAzmVar.set(limits[3])

            Label1=tk.Label(topLims)
            Label1.place(relx=0.25,rely=0.05,height=21,width=43)
            Label1.configure(text='Min')
            Label1.configure(anchor='w')

            Label2=tk.Label(topLims)
            Label2.place(relx=0.62,rely=0.05,height=21,width=43)
            Label2.configure(text='Max')
            Label2.configure(anchor='w')

            Label3=tk.Label(topLims)
            Label3.place(relx=0.05,rely=0.25,height=21,width=80 )
            Label3.configure(text='Altitude')
            Label3.configure(anchor='w')

            Entry1=tk.Entry(topLims)
            Entry1.place(relx=0.25,rely=0.25,height=25,relwidth=0.35)
            Entry1.configure(background=colors['bg'])
            Entry1.configure(fg=colors['text'])
            if colors['text']=='red':
                Entry1.configure(selectbackground=colors['select_bg'])
                Entry1.configure(selectforeground=colors['select_text'])
            Entry1.configure(textvariable=minAltVar)

            Entry2=tk.Entry(topLims)
            Entry2.place(relx=0.62,rely=0.25,height=25,relwidth=0.35)
            Entry2.configure(background=colors['bg'])
            Entry2.configure(fg=colors['text'])
            if colors['text']=='red':
                Entry2.configure(selectbackground=colors['select_bg'])
                Entry2.configure(selectforeground=colors['select_text'])
            Entry2.configure(textvariable=maxAltVar)

            Label4=tk.Label(topLims)
            Label4.place(relx=0.05,rely=0.45,height=21,width=80)
            Label4.configure(text='Azimut')
            Label4.configure(anchor='w')

            Entry3=tk.Entry(topLims)
            Entry3.place(relx=0.25,rely=0.45,height=25,relwidth=0.35)
            Entry3.configure(background=colors['bg'])
            Entry3.configure(fg=colors['text'])
            if colors['text']=='red':
                Entry3.configure(selectbackground=colors['select_bg'])
                Entry3.configure(selectforeground=colors['select_text'])
            Entry3.configure(textvariable=minAzmVar)

            Entry4=tk.Entry(topLims)
            Entry4.place(relx=0.62,rely=0.45,height=25,relwidth=0.35)
            Entry4.configure(background=colors['bg'])
            Entry4.configure(fg=colors['text'])
            if colors['text']=='red':
                Entry4.configure(selectbackground=colors['select_bg'])
                Entry4.configure(selectforeground=colors['select_text'])
            Entry4.configure(textvariable=maxAzmVar)

            Button2=tk.Button(topLims)
            Button2.place(relx=0.45,rely=0.7,height=29,width=58)
            Button2.configure(text='Save')
            Button2.configure(command=saveLims)

        def saveSite():
            try:
                if ':' in siteLatVar.get(): lat=stars.readDMS(siteLatVar.get(),deg=True)
                else: lat=float(siteLatVar.get())
            except:
                messagebox.showerror('Latitude Error','Wrong Latitude format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
                topSite.lift()
                return
            try:
                if ':' in siteLonVar.get(): lon=stars.readDMS(siteLonVar.get(),deg=True)
                else: lon=float(siteLonVar.get())
            except:
                messagebox.showerror('Longitude Error','Wrong Longitude format! Correct format is "D:M:S" or "D.d" (decimal number in degrees).')
                topSite.lift()
                return
            if site is not None: del settings1['sites'][site]
            settings1['sites'][siteNameVar.get()]=siteClass(siteNameVar.get(),lat,lon,float(siteEleVar.get()),limits)
            TCombobox2['values']=sorted(settings1['sites'].keys())
            TCombobox2.current(sorted(settings1['sites'].keys()).index(siteNameVar.get()))
            Button2_1.configure(state=tk.NORMAL)
            Button2_2.configure(state=tk.NORMAL)
            topSite.destroy()
            top.lift()

        topSite=tk.Tk()
        topSite.lift()
        topSite.geometry('230x200')
        topSite.title('Site')
        try: topSite.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        topSite.resizable(False,False)

        siteNameVar=tk.StringVar(topSite)
        siteLatVar=tk.StringVar(topSite)
        siteLonVar=tk.StringVar(topSite)
        siteEleVar=tk.StringVar(topSite)
        new_limits=[0,90,0,360]
        limits=new_limits

        if site is not None:
            siteNameVar.set(site)
            siteLatVar.set(stars.printDMS(settings1['sites'][site].lat))
            siteLonVar.set(stars.printDMS(settings1['sites'][site].lon))
            siteEleVar.set(settings1['sites'][site].ele)
            limits=settings1['sites'][site].limits

        Label1=tk.Label(topSite)
        Label1.place(relx=0.05,rely=0.05,height=21,width=43)
        Label1.configure(text='Name')
        Label1.configure(anchor='w')

        Entry1=tk.Entry(topSite)
        Entry1.place(relx=0.35,rely=0.05,height=25,relwidth=0.6)
        Entry1.configure(background=colors['bg'])
        Entry1.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry1.configure(selectbackground=colors['select_bg'])
            Entry1.configure(selectforeground=colors['select_text'])
        Entry1.configure(textvariable=siteNameVar)

        Label2=tk.Label(topSite)
        Label2.place(relx=0.05,rely=0.25,height=21,width=57)
        Label2.configure(text='Latitude')
        Label2.configure(anchor='w')

        Entry2=tk.Entry(topSite)
        Entry2.place(relx=0.35,rely=0.25,height=25,relwidth=0.6)
        Entry2.configure(background=colors['bg'])
        Entry2.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry2.configure(selectbackground=colors['select_bg'])
            Entry2.configure(selectforeground=colors['select_text'])
        Entry2.configure(textvariable=siteLatVar)

        Label3=tk.Label(topSite)
        Label3.place(relx=0.05,rely=0.45,height=21,width=68)
        Label3.configure(text='Longitude')
        Label3.configure(anchor='w')

        Entry3=tk.Entry(topSite)
        Entry3.place(relx=0.35,rely=0.45,height=25,relwidth=0.6)
        Entry3.configure(background=colors['bg'])
        Entry3.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry3.configure(selectbackground=colors['select_bg'])
            Entry3.configure(selectforeground=colors['select_text'])
        Entry3.configure(textvariable=siteLonVar)

        Label4=tk.Label(topSite)
        Label4.place(relx=0.05,rely=0.65,height=21,width=65)
        Label4.configure(text='Elevation')
        Label4.configure(anchor='w')

        Entry4=tk.Entry(topSite)
        Entry4.place(relx=0.35,rely=0.65,height=25,relwidth=0.6)
        Entry4.configure(background=colors['bg'])
        Entry4.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry4.configure(selectbackground=colors['select_bg'])
            Entry4.configure(selectforeground=colors['select_text'])
        Entry4.configure(textvariable=siteEleVar)

        Button1=tk.Button(topSite)
        Button1.place(relx=0.2,rely=0.82,height=29,width=58)
        Button1.configure(text='Limits')
        Button1.configure(command=setLimits)

        Button2=tk.Button(topSite)
        Button2.place(relx=0.6,rely=0.82,height=29,width=58)
        Button2.configure(text='Save')
        Button2.configure(command=saveSite)

    def editSite():
        addSite(siteVar.get())

    def delSite():
        del settings1['sites'][siteVar.get()]
        TCombobox2['values']=sorted(settings1['sites'])
        if len(TCombobox2['values'])==0:
            Button2_1.configure(state=tk.DISABLED)
            Button2_2.configure(state=tk.DISABLED)
            TCombobox2.set('')
        else: TCombobox2.current(0)

    def addTel(tel=None):
        def saveTel():
            if tel is not None: settings1['telescopes'].remove(tel)
            settings1['telescopes'].append(telNameVar.get())
            TCombobox3['values']=sorted(settings1['telescopes'])
            TCombobox3.current(sorted(settings1['telescopes']).index(telNameVar.get()))
            Button3_1.configure(state=tk.NORMAL)
            Button3_2.configure(state=tk.NORMAL)
            topTel.destroy()
            top.lift()

        topTel=tk.Tk()
        topTel.lift()
        topTel.geometry('400x80')
        topTel.title('Telescope')
        try: topTel.iconbitmap('ObsPlanner.ico')   #win
        except: pass
        topTel.resizable(False,False)

        telNameVar=tk.StringVar(topTel)

        if tel is not None: telNameVar.set(tel)

        Label1=tk.Label(topTel)
        Label1.place(relx=0.01,rely=0.1,height=21,width=43)
        Label1.configure(text='Name')

        Entry1=tk.Entry(topTel)
        Entry1.place(relx=0.15,rely=0.1,height=25,relwidth=0.82)
        Entry1.configure(background=colors['bg'])
        Entry1.configure(fg=colors['text'])
        if colors['text']=='red':
            Entry1.configure(selectbackground=colors['select_bg'])
            Entry1.configure(selectforeground=colors['select_text'])
        Entry1.configure(textvariable=telNameVar)

        Button1=tk.Button(topTel)
        Button1.place(relx=0.4,rely=0.6,height=24,width=60)
        Button1.configure(text='Save')
        Button1.configure(command=saveTel)

    def editTel():
        addTel(telVar.get())

    def delTel():
        settings1['telescopes'].remove(telVar.get())
        TCombobox3['values']=sorted(settings1['telescopes'])
        if len(TCombobox3['values'])==0:
            Button3_1.configure(state=tk.DISABLED)
            Button3_2.configure(state=tk.DISABLED)
            TCombobox3.set('')
        else: TCombobox3.current(0)

    def saveSet():
        global settings,noSett,changed
        if len(observerVar.get())==0:
            messagebox.showerror('Observer Error','No default observer! Please, add one!')
            top.lift()
            return
        if len(siteVar.get())==0:
            messagebox.showerror('Site Error','No default site! Please, add one!')
            top.lift()
            return
        if len(telVar.get())==0:
            messagebox.showerror('Telescope Error','No default telescope! Please, add one!')
            top.lift()
            return
        settings1['default_obs']=observerVar.get()
        settings1['default_site']=settings1['sites'][siteVar.get()]
        settings1['default_tel']=telVar.get()
        if not (settings1['file_copy']==bool(copyVar.get())):
            messagebox.showinfo('Images','New image location will be applied only on new images. Old images are displayed from old location.')
        settings1['file_copy']=bool(copyVar.get())
        if not (settings1['night_mode']==bool(nightVar.get())):
            messagebox.showinfo('Colors','Changes of color mode will be applied after restart of ObsPlanner.')
        settings1['night_mode']=bool(nightVar.get())
        settings=copy.deepcopy(settings1)
        noSett=False

        if len(objects.objects.keys())>0:
            zoznam=objfilter()
            try:
                if objZ.name in zoznam:
                    fake=fakeEvt(zoznam.index(objZ.name),zoznam)
                    objselect(fake)
                else:
                    changed0=changed
                    clear()
                    changed=changed0
            except: pass #nebol zvoleny objekt

        top.destroy()
        root.lift()

    top=tk.Tk()
    top.lift()
    top.geometry('530x200')
    top.title('Settings')
    try: top.iconbitmap('ObsPlanner.ico')   #win
    except: pass
    top.resizable(False,False)

    settings1=copy.deepcopy(settings)

    observerVar=tk.StringVar(top)
    siteVar=tk.StringVar(top)
    telVar=tk.StringVar(top)
    copyVar=tk.IntVar(top)
    nightVar=tk.IntVar(top)

    Label1=tk.Label(top)
    Label1.place(relx=0.02,rely=0.01,height=21,width=120)
    Label1.configure(text='Default Observer')
    Label1.configure(anchor='w')

    if colors['text']=='red':
        top.option_add('*TCombobox*Listbox*Background',colors['bg'])
        top.option_add('*TCombobox*Listbox*Foreground',colors['text'])
    style=ttk.Style(top)
    style.map('TCombobox',selectbackground=[('readonly',colors['bg'])])
    style.map('TCombobox',fieldbackground=[('readonly',colors['bg'])])
    style.map('TCombobox',foreground=[('readonly',colors['text'])])
    style.map('TCombobox',selectforeground=[('readonly',colors['text'])])

    TCombobox1=ttk.Combobox(top)
    TCombobox1.place(relx=0.26,rely=0.01,height=25,relwidth=0.4)
    TCombobox1.configure(textvariable=observerVar)
    TCombobox1.configure(takefocus='')
    TCombobox1.configure(state='readonly')
    if len(settings1['observers'])>0:
        TCombobox1['values']=sorted(settings1['observers'])
        TCombobox1.current(sorted(settings1['observers']).index(settings1['default_obs']))

    Button1=tk.Button(top)
    Button1.place(relx=0.69,rely=0.01,height=24,width=50)
    Button1.configure(text='Add')
    Button1.configure(command=addObserver)

    Button1_1=tk.Button(top)
    Button1_1.place(relx=0.79,rely=0.01,height=24,width=50)
    Button1_1.configure(text='Edit')
    Button1_1.configure(command=editObserver)
    if len(TCombobox1['values'])==0: Button1_1.configure(state=tk.DISABLED)

    Button1_2=tk.Button(top)
    Button1_2.place(relx=0.89,rely=0.01,height=24,width=50)
    Button1_2.configure(text='Delete')
    Button1_2.configure(command=delObserver)
    if len(TCombobox1['values'])==0: Button1_2.configure(state=tk.DISABLED)

    Label2=tk.Label(top)
    Label2.place(relx=0.02,rely=0.18,height=21,width=90)
    Label2.configure(text='Default Site')
    Label2.configure(anchor='w')

    TCombobox2=ttk.Combobox(top)
    TCombobox2.place(relx=0.26,rely=0.18,height=25,relwidth=0.4)
    TCombobox2.configure(textvariable=siteVar)
    TCombobox2.configure(takefocus='')
    TCombobox2.configure(state='readonly')
    if len(settings1['sites'])>0:
        TCombobox2['values']=sorted(settings1['sites'].keys())
        TCombobox2.current(sorted(settings1['sites'].keys()).index(settings1['default_site'].name))

    Button2=tk.Button(top)
    Button2.place(relx=0.69,rely=0.18,height=24,width=50)
    Button2.configure(text='Add')
    Button2.configure(command=addSite)

    Button2_1=tk.Button(top)
    Button2_1.place(relx=0.79,rely=0.18,height=24,width=50)
    Button2_1.configure(text='Edit')
    Button2_1.configure(command=editSite)
    if len(TCombobox2['values'])==0: Button2_1.configure(state=tk.DISABLED)

    Button2_2=tk.Button(top)
    Button2_2.place(relx=0.89,rely=0.18,height=24,width=50)
    Button2_2.configure(text='Delete')
    Button2_2.configure(command=delSite)
    if len(TCombobox2['values'])==0: Button2_2.configure(state=tk.DISABLED)

    Label3=tk.Label(top)
    Label3.place(relx=0.02,rely=0.35,height=21,width=125)
    Label3.configure(text='Default Telescope')
    Label3.configure(anchor='w')

    TCombobox3=ttk.Combobox(top)
    TCombobox3.place(relx=0.26,rely=0.35,height=25,relwidth=0.4)
    TCombobox3.configure(textvariable=telVar)
    TCombobox3.configure(takefocus='')
    TCombobox3.configure(state='readonly')
    if len(settings1['telescopes'])>0:
        TCombobox3['values']=sorted(settings1['telescopes'])
        TCombobox3.current(sorted(settings1['telescopes']).index(settings1['default_tel']))

    Button3=tk.Button(top)
    Button3.place(relx=0.69,rely=0.35,height=24,width=50)
    Button3.configure(text='Add')
    Button3.configure(command=addTel)

    Button3_1=tk.Button(top)
    Button3_1.place(relx=0.79,rely=0.35,height=24,width=50)
    Button3_1.configure(text='Edit')
    Button3_1.configure(command=editTel)
    if len(TCombobox3['values'])==0: Button3_1.configure(state=tk.DISABLED)

    Button3_2=tk.Button(top)
    Button3_2.place(relx=0.89,rely=0.35,height=24,width=50)
    Button3_2.configure(text='Delete')
    Button3_2.configure(command=delTel)
    if len(TCombobox3['values'])==0: Button3_2.configure(state=tk.DISABLED)

    Label4=tk.Label(top)
    Label4.place(relx=0.02,rely=0.52,height=21,width=78)
    Label4.configure(text='Image Path')
    Label4.configure(anchor='w')

    Radiobutton1=tk.Radiobutton(top)
    Radiobutton1.place(relx=0.26,rely=0.52,height=21,relwidth=0.2)
    Radiobutton1.configure(justify=tk.LEFT)
    Radiobutton1.configure(text='Original')
    Radiobutton1.configure(variable=copyVar)
    Radiobutton1.configure(value=0)

    Radiobutton2=tk.Radiobutton(top)
    Radiobutton2.place(relx=0.46,rely=0.52,height=21,relwidth=0.25)
    Radiobutton2.configure(justify=tk.LEFT)
    Radiobutton2.configure(text='Copy locally')
    Radiobutton2.configure(variable=copyVar)
    Radiobutton2.configure(value=1)

    if settings1['file_copy']: copyVar.set(1)
    else: copyVar.set(0)

    Label5=tk.Label(top)
    Label5.place(relx=0.02,rely=0.69,height=21,width=78)
    Label5.configure(text='Colors')
    Label5.configure(anchor='w')

    Radiobutton3=tk.Radiobutton(top)
    Radiobutton3.place(relx=0.26,rely=0.69,height=21,relwidth=0.22)
    Radiobutton3.configure(justify=tk.LEFT)
    Radiobutton3.configure(text='Day Mode')
    Radiobutton3.configure(variable=nightVar)
    Radiobutton3.configure(value=0)

    Radiobutton4=tk.Radiobutton(top)
    Radiobutton4.place(relx=0.48,rely=0.69,height=21,relwidth=0.22)
    Radiobutton4.configure(justify=tk.LEFT)
    Radiobutton4.configure(text='Night Mode')
    Radiobutton4.configure(variable=nightVar)
    Radiobutton4.configure(value=1)

    if settings1['night_mode']: nightVar.set(1)
    else: nightVar.set(0)

    Button4=tk.Button(top)
    Button4.place(relx=0.40,rely=0.86,height=24,width=60)
    Button4.configure(text='Save')
    Button4.configure(command=saveSet)

def clear():
    '''reset state of buttons, lists, figures...'''
    global changed
    objfilter()
    obssVar.set('')
    Text1.delete(1.0,tk.END)
    Text2.delete(1.0,tk.END)
    figAlt.clf()
    figObj.clf()
    canvas1.draw()
    canvas2.draw()
    Button2.configure(state=tk.DISABLED)
    Button3.configure(state=tk.DISABLED)
    Button4.configure(state=tk.DISABLED)
    Button5.configure(state=tk.DISABLED)
    Button6.configure(state=tk.DISABLED)
    changed=True

def saveQuestion():
    '''ask if save objects on changing'''
    global changed
    global objects
    if changed:
        ans=messagebox.askquestion('ObsPlanner','Save objects to file?',type='yesnocancel')
        if ans=='yes':
            if len(settings['file'])==0:
                name=filedialog.asksaveasfilename(parent=root,filetypes=[('ObsPlanner files','*.opd'),('All files','*.*')],\
                title='Save file',defaultextension='.opd')
                name=name.replace('\\','/')
                if len(name)>0:
                    cwd=os.getcwd().replace('\\','/')+'/'
                    if cwd in name: name=name.replace(cwd,'')    #uloz relativnu cestu
                    settings['file']=name
                else: return 0
            objects.save(settings['file'])
        elif ans=='cancel': return 0
        changed=False

def join():
    global objects
    if saveQuestion()==0: return  #zrusene

    name1=filedialog.askopenfilename(parent=root,filetypes=[('ObsPlanner files','*.opd'),('All files','*.*')],title='Open file - 1st file')
    name1=name1.replace('\\','/')

    name2=filedialog.askopenfilename(parent=root,filetypes=[('ObsPlanner files','*.opd'),('All files','*.*')],title='Open file - 2nd file')
    name2=name2.replace('\\','/')

    if len(name1)*len(name2)>0:
        objects=objects_import.join(name1,name2)
        clear()
        settings['file']=''

def maximI():
    global objects
    if saveQuestion()==0: return  #zrusene

    name=filedialog.askopenfilename(parent=root,filetypes=[('MaximDL catalog','stars.csv'),('All files','*.*')],title='Import from MaximDL')
    name=name.replace('\\','/')

    if len(name)>0:
        objects=objects_import.maximI(name)
        clear()
        settings['file']=''

def sipsI():
    global objects
    if saveQuestion()==0: return  #zrusene

    name=filedialog.askopenfilename(parent=root,filetypes=[('SIPS catalog','catalog.ini'),('All files','*.*')],title='Import from SIPS')
    name=name.replace('\\','/')

    if len(name)>0:
        objects=objects_import.sipsI(name)
        clear()
        settings['file']=''

def maximE():
    zoznam=list(objsVar.get())
    objE={}
    for o in zoznam: objE[o]=objects.objects[o]
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('MaximDL catalog','stars.csv'),('All files','*.*')],title='Export to MaximDL',\
        defaultextension='.csv',initialfile='stars.csv')
    if len(name)>0: objects_import.maximE(objE,name)

def sipsE():
    zoznam=list(objsVar.get())
    objE={}
    for o in zoznam: objE[o]=objects.objects[o]
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('SIPS catalog','catalog.ini'),('All files','*.*')],title='Export to SIPS',\
        defaultextension='.ini',initialfile='catalog.ini')
    if len(name)>0: objects_import.sipsE(objE,name)

def aptE():
    zoznam=list(objsVar.get())
    objE={}
    for o in zoznam: objE[o]=objects.objects[o]
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('APT native format','APT_CustomObjectsList.xml'),('All files','*.*')],title='Export to APT',\
        defaultextension='.xml',initialfile='APT_CustomObjectsList.xml')
    if len(name)>0: objects_import.aptE(objE,name)

def textE():
    zoznam=list(objsVar.get())
    objE={}
    for o in zoznam: objE[o]=objects.objects[o]
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('Text file','*.txt'),('All files','*.*')],title='Export to TextFile',\
        defaultextension='.txt')
    if len(name)>0: objects_import.textE(objE,name)

def excelE():
    zoznam=list(objsVar.get())
    year,mon,day,hour,minute,sec=getDate()
    objE={}
    for o in zoznam: objE[o]=objects.objects[o]
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('Excel file','*.xls'),('All files','*.*')],title='Export to Excel File',\
        defaultextension='.xls')
    if len(name)>0: objects_import.excelE(objE,name,stars.juldat(year,mon,day,hour,minute,sec),stars.juldat(year,mon,day+round(hour/24.),0,0,0),\
    settings['default_site'].lon,settings['default_site'].lat)

def textObsE(allObj=False):
    if allObj: zoznam=list(objsVar.get())
    else: zoznam=[objZ.name]
    objE={}
    for o in zoznam: objE[o]=objects.objects[o]
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('Text file','*.txt'),('All files','*.*')],title='Export Observations to TextFile',\
        defaultextension='.txt')
    if len(name)>0: objects_import.textObsE(objE,name)

def textObsAllE():
    textObsE(allObj=True)

def excelObsE(allObj=False):
    if allObj: zoznam=list(objsVar.get())
    else: zoznam=[objZ.name]
    objE={}
    for o in zoznam: objE[o]=objects.objects[o]
    name=filedialog.asksaveasfilename(parent=root,filetypes=[('Excel file','*.xls'),('All files','*.*')],title='Export Observations to Excel File',\
        defaultextension='.xls')
    if len(name)>0: objects_import.excelObsE(objE,name)

def excelObsAllE():
    excelObsE(allObj=True)

def ShowImg():
    #test+warnign ci subor existuje
    subor=obsZ1.image
    if not os.path.isfile(subor):
        if os.path.isfile(os.getcwd().replace('\\','/')+'/'+obsZ1.image):
            subor=os.getcwd().replace('\\','/')+'/'+obsZ1.image     #problem s relativnou cestou vo Win
        else:
            messagebox.showerror('ObsPlanner','Image "'+subor+'" not found!')
            return
    #open image in default software
    if sys.platform=='linux' or sys.platform=='linux2':
        myEnv = dict(os.environ)
        lp_key = 'LD_LIBRARY_PATH'
        lp_orig = myEnv.get(lp_key + '_ORIG')
        if lp_orig is not None: myEnv[lp_key] = lp_orig
        else: lp = myEnv.get(lp_key)
        if lp is not None: myEnv.pop(lp_key)
        subprocess.call(['xdg-open',subor],env=myEnv)       #call
    else:
        try: os.startfile(subor)
        except: os.startfile(os.getcwd().replace('\\','/')+'/'+obsZ1.image)     #problem s relativnou cestou vo Win

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
    set_foregroundcolor(ax,colors['fig_text'])
    #vyznacenie limitov
    rect=patches.Rectangle((-10,0),380,100,edgecolor='none',facecolor=colors['fig_shade'])
    ax.add_patch(rect)
    rect=patches.Rectangle((settings['default_site'].limits[2],settings['default_site'].limits[0]),\
        settings['default_site'].limits[3]-settings['default_site'].limits[2],\
        settings['default_site'].limits[1]-settings['default_site'].limits[0],linewidth=1,edgecolor=colors['fig_edge'],facecolor=colors['fig_bg'])
    ax.add_patch(rect)

    year,mon,day,hour,minute,sec=getDate()
    jd0=stars.juldat(year,mon,day,hour-2,minute,sec)  #start -2h
    jd1=stars.juldat(year,mon,day,hour+8,minute,sec)  #stop +8h
    jd=np.linspace(jd0,jd1,200)

    a,h=objZ.altAz(jd,settings['default_site'].lon,settings['default_site'].lat)
    if max(h)<0:
        figAlt.clf()
        ax=figAlt.add_subplot(111)
        ax.text(0,0,'Below horizont!',horizontalalignment='center',verticalalignment='center',fontsize=30,color=colors['fig_text'])
        ax.set_xlim(-0.5,0.5)
        ax.set_ylim(-0.5,0.5)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(False)
        ax.set_axis_off()
        canvas2.draw()
        return
    h0=np.ma.array(h[np.where(h>-5)])
    a0=np.ma.array(a[np.where(h>-5)])
    i=np.where((np.abs(np.diff(a0))>10)*(np.abs(np.diff(np.sign(a0-300)))>0))[0]   #prechod cez N=360
    a0[i]=np.ma.masked
    h0[i]=np.ma.masked
    ax.plot(a0,h0,colors['fig_text']+'-')

    ax.set_xlim(min(a0)-5,max(a0)+5)
    ax.set_ylim(max(0,min(h0)-5),max(h)+5)

    #znacky po hodinach
    jdH=np.arange(stars.juldat(year,mon,day,hour-1,0,0),stars.juldat(year,mon,day,hour+7,0,1),1./24.)
    for i in range(len(jdH)):
        a,h=objZ.altAz(jdH[i],settings['default_site'].lon,settings['default_site'].lat)
        if h>0:
            ax.plot(a,h,colors['fig_text']+'o')
            if hour-1+i>=24:
                t=ax.text(a,h-(max(h0)-max(0,min(h0)))/10.,hour-1+i-24,color=colors['fig_text'])
                t.set_path_effects([PathEffects.withStroke(linewidth=2,foreground=colors['fig_bg'])])
            else:
                t=ax.text(a,h-(max(h0)-max(0,min(h0)))/10.,hour-1+i,color=colors['fig_text'])
                t.set_path_effects([PathEffects.withStroke(linewidth=2,foreground=colors['fig_bg'])])

    #aktualna poloha
    jd=stars.juldat(year,mon,day,hour,minute,sec)
    a,h=objZ.altAz(jd,settings['default_site'].lon,settings['default_site'].lat)
    ax.plot(a,h,colors['fig_text']+'x',markersize=12)

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
            if (a<settings['default_site'].limits[3]) and (a>settings['default_site'].limits[2]) and (h<settings['default_site'].limits[1])\
             and (h>settings['default_site'].limits[0]):
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
                if (a<settings['default_site'].limits[3]) and (a>settings['default_site'].limits[2]) and \
                (h<settings['default_site'].limits[1]) and (h>settings['default_site'].limits[0]):
                    zoznam.append(ob['object'].name)
    zoznam=sort(zoznam)
    objsVar.set(zoznam)

    if len(zoznam)>0: import_export.entryconfig('Export Selected Objects',state='normal')
    else: import_export.entryconfig('Export Selected Objects',state='disabled')

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
    constellations[objZ.const].plotObject(objZ.ra,objZ.dec,colors,figObj)
    canvas1.draw()

    plotAlt(objZ.ra,objZ.dec)

    year,mon,day,hour,minute,sec=getDate()
    Text1.delete(1.0,tk.END)
    Text2.delete(1.0,tk.END)
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
    print('Transit: '+stars.printDMS(t)+' @ '+str(round(objZ.dec+90-settings['default_site'].lat,2))+' deg')
    print('Set: '+s)
    print('---------------------')
    print('Note: '+objZ.note)
    sys.stdout=old

    obssVar.set(sortObs(obsZ))
    Button2.configure(state=tk.NORMAL)
    Button3.configure(state=tk.NORMAL)
    Button4.configure(state=tk.NORMAL)
    Button5.configure(state=tk.DISABLED)
    Button6.configure(state=tk.DISABLED)
    Button7.configure(state=tk.DISABLED)

    if len(obsZ)>0: import_export.entryconfig('Export Observations of Object',state='normal')
    else: import_export.entryconfig('Export Observations of Object',state='disabled')

def obsselect(evt):
    global obsZ1  #zobrazene pozorovanie
    if len(obsZ)==0: return
    w=evt.widget
    if len(w.curselection())==0: return
    index=int(w.curselection()[0])
    value=w.get(index)

    obsZ1=obsZ[value]
    Text2.delete(1.0,tk.END)
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

    Button5.configure(state=tk.NORMAL)
    Button6.configure(state=tk.NORMAL)

    if len(obsZ1.image)>0: Button7.configure(state=tk.NORMAL)
    else: Button7.configure(state=tk.DISABLED)

changed=False

constellations=stars.load()
objects=objClass.objects(constellations)

#nastavenia
if os.path.isfile('data/settings.ops'):
    f=open('data/settings.ops','rb')
    settings=pickle.load(f)
    f.close()
    if os.path.isfile(settings['file'].strip()): objects.load(settings['file'].strip())
    noSett=False
    if 'file_copy' not in settings: settings['file_copy']=False
else:
    settings={}
    settings['observers']=[]
    settings['sites']={}
    settings['telescopes']=[]
    settings['default_obs']=''
    settings['default_site']=None
    settings['default_tel']=''
    settings['file']=''
    settings['file_copy']=False
    settings['night_mode']=False
    noSett=True
settings0=copy.deepcopy(settings)

#load colors
if settings['night_mode']: color_name='data/night.opc'
else: color_name='data/day.opc'
f=open(color_name,'rb')
colors=pickle.load(f)
f.close()

#graphs
figObj=Figure(facecolor=colors['fig_bg'])
figAlt=Figure(facecolor=colors['fig_bg'])


if not os.path.isdir('images'): os.mkdir('images')

root=tk.Tk()
root.protocol('WM_DELETE_WINDOW',Exit)
try: root.state('zoomed')  #win
except:
    try: root.attributes('-zoomed',True)  #linux
    except: pass

root.geometry('800x500')
root.title('ObsPlanner')
try: root.iconbitmap('ObsPlanner.ico')   #win
except: pass
root.configure(background=colors['window'])

#premenne pre gui
objsVar=tk.Variable(root)
objInfoVar=tk.StringVar(root)
obssVar=tk.Variable(root)
dateVar=tk.StringVar(root)
filtVar=tk.StringVar(root)

#objekty
Labelframe0=tk.LabelFrame(root)
Labelframe0.place(relx=0.01,rely=0.02,relheight=0.96,relwidth=0.34)
Labelframe0.configure(text='Objects')
Labelframe0.configure(width=280)
Labelframe0.configure(background=colors['window'])
Labelframe0.configure(fg=colors['text'])

Label1=tk.Label(Labelframe0)
Label1.place(relx=0.04,rely=0.01,height=21,width=39)
Label1.configure(text='Show')
Label1.configure(background=colors['window'])
Label1.configure(fg=colors['text'])

if colors['text']=='red':
    root.option_add('*TCombobox*Listbox*Foreground',colors['text'])
    root.option_add('*TCombobox*Listbox*Background',colors['bg'])
style=ttk.Style()
style.map('TCombobox',selectbackground=[('readonly',colors['bg'])])
style.map('TCombobox',fieldbackground=[('readonly',colors['bg'])])
style.map('TCombobox',foreground=[('readonly',colors['text'])])
style.map('TCombobox',selectforeground=[('readonly',colors['text'])])

TCombobox1=ttk.Combobox(Labelframe0)
TCombobox1.place(relx=0.2,rely=0.01,height=25,relwidth=0.7)
TCombobox1.configure(textvariable=filtVar)
TCombobox1.configure(state='readonly')
#TCombobox1.configure(background=colors['bg'])
#TCombobox1.configure(fg=colors['text'])
TCombobox1['values']=('All','Visible','Above horizont','Observed','Not Observed','Visible + Not Observed')
TCombobox1.current(0)
TCombobox1.bind('<<ComboboxSelected>>',objfilter)

Scrolledlistbox1=ScrolledListBox(Labelframe0)
Scrolledlistbox1.place(relx=0.04,rely=0.08,relheight=0.44,relwidth=0.92)
Scrolledlistbox1.configure(background=colors['bg'])
Scrolledlistbox1.configure(fg=colors['text'])
if colors['text']=='red':
    Scrolledlistbox1.configure(selectbackground=colors['select_bg'])
    Scrolledlistbox1.configure(selectforeground=colors['select_text'])
#Scrolledlistbox1.configure(inactiveselectbackground=colors['select_bg'])
Scrolledlistbox1.configure(width=10)
Scrolledlistbox1.configure(listvariable=objsVar)
Scrolledlistbox1.bind('<<ListboxSelect>>',objselect)

Text1=ScrolledText(Labelframe0)
Text1.place(relx=0.04,rely=0.54,relheight=0.4,relwidth=0.92)
Text1.configure(background=colors['bg'])
Text1.configure(fg=colors['text'])
if colors['text']=='red':
    Text1.configure(selectbackground=colors['select_bg'])
    Text1.configure(selectforeground=colors['select_text'])
    Text1.configure(inactiveselectbackground=colors['select_bg'])
Text1.configure(width=256)
Text1.configure(wrap=tk.WORD)

#TODO focus color?, disabled color?
Button3_2=tk.Button(Labelframe0)
Button3_2.place(relx=0.05,rely=0.95,height=24,width=47)
Button3_2.configure(command=AddObj)
Button3_2.configure(text='Add')
Button3_2.configure(background=colors['bg'])
Button3_2.configure(fg=colors['text'])

Button2=tk.Button(Labelframe0)
Button2.place(relx=0.35,rely=0.95,height=24,width=47)
Button2.configure(command=EditObj)
Button2.configure(text='Edit')
Button2.configure(background=colors['bg'])
Button2.configure(fg=colors['text'])
Button2.configure(state=tk.DISABLED)

Button3=tk.Button(Labelframe0)
Button3.place(relx=0.65,rely=0.95,height=24,width=47)
Button3.configure(command=DelObj)
Button3.configure(text='Delete')
Button3.configure(background=colors['bg'])
Button3.configure(fg=colors['text'])
Button3.configure(state=tk.DISABLED)

#pozorovania
Labelframe1=tk.LabelFrame(root)
Labelframe1.place(relx=0.36,rely=0.02,relheight=0.96,relwidth=0.3)
Labelframe1.configure(text='Observations')
Labelframe1.configure(width=250)
Labelframe1.configure(background=colors['window'])
Labelframe1.configure(fg=colors['text'])

Scrolledlistbox2=ScrolledListBox(Labelframe1)
Scrolledlistbox2.place(relx=0.04,rely=0.01,relheight=0.51,relwidth=0.92)
Scrolledlistbox2.configure(background=colors['bg'])
Scrolledlistbox2.configure(fg=colors['text'])
if colors['text']=='red':
    Scrolledlistbox2.configure(selectbackground=colors['select_bg'])
    Scrolledlistbox2.configure(selectforeground=colors['select_text'])
#Scrolledlistbox2.configure(inactiveselectbackground=colors['select_bg'])
Scrolledlistbox2.configure(width=10)
Scrolledlistbox2.configure(listvariable=obssVar)
Scrolledlistbox2.bind('<<ListboxSelect>>',obsselect)

Text2=ScrolledText(Labelframe1)
Text2.place(relx=0.04,rely=0.54,relheight=0.4,relwidth=0.92)
Text2.configure(background=colors['bg'])
Text2.configure(fg=colors['text'])
if colors['text']=='red':
    Text2.configure(selectbackground=colors['select_bg'])
    Text2.configure(selectforeground=colors['select_text'])
    Text2.configure(inactiveselectbackground=colors['select_bg'])
Text2.configure(width=234)
Text2.configure(wrap=tk.WORD)

Button4=tk.Button(Labelframe1)
Button4.place(relx=0.02,rely=0.95,height=24,width=47)
Button4.configure(command=AddObs)
Button4.configure(text='Add')
Button4.configure(background=colors['bg'])
Button4.configure(fg=colors['text'])
Button4.configure(state=tk.DISABLED)

Button5=tk.Button(Labelframe1)
Button5.place(relx=0.28,rely=0.95,height=24,width=47)
Button5.configure(command=EditObs)
Button5.configure(text='Edit')
Button5.configure(background=colors['bg'])
Button5.configure(fg=colors['text'])
Button5.configure(state=tk.DISABLED)

Button6=tk.Button(Labelframe1)
Button6.place(relx=0.53,rely=0.95,height=24,width=47)
Button6.configure(command=DelObs)
Button6.configure(text='Delete')
Button6.configure(background=colors['bg'])
Button6.configure(fg=colors['text'])
Button6.configure(state=tk.DISABLED)

Button7=tk.Button(Labelframe1)
Button7.place(relx=0.78,rely=0.95,height=24,width=47)
Button7.configure(command=ShowImg)
Button7.configure(state=tk.DISABLED)
Button7.configure(background=colors['bg'])
Button7.configure(fg=colors['text'])
Button7.configure(text='Image')

#obrazky a datum
Label0=tk.Label(root)
Label0.place(relx=0.68,rely=0.02,height=21,width=130)
Label0.configure(text='UTC Date&Time')
Label0.configure(background=colors['window'])
Label0.configure(fg=colors['text'])

Entry1=tk.Entry(root)
Entry1.place(relx=0.78,rely=0.02,height=25,relwidth=0.12)
Entry1.configure(background=colors['bg'])
Entry1.configure(fg=colors['text'])
if colors['text']=='red':
    Entry1.configure(selectbackground=colors['select_bg'])
    Entry1.configure(selectforeground=colors['select_text'])
Entry1.configure(textvariable=dateVar)

Button1=tk.Button(root)
Button1.place(relx=0.92,rely=0.02,height=24,width=55)
Button1.configure(command=NowTime)
Button1.configure(background=colors['bg'])
Button1.configure(fg=colors['text'])
Button1.configure(text='Now')

frame2=tk.Frame(root)
frame2.place(relx=0.68,rely=0.08,relheight=0.44,relwidth=0.3)
canvas2=FigureCanvasTkAgg(figAlt,frame2)
canvas2.get_tk_widget().pack(side='top',fill='both',expand=1)

frame1=tk.Frame(root)
frame1.place(relx=0.68,rely=0.54,relheight=0.44,relwidth=0.3)
canvas1=FigureCanvasTkAgg(figObj,frame1)
canvas1.get_tk_widget().pack(side='top',fill='both',expand=1)

#TODO focus color?, disabled color?
#menu
Popupmenu1=tk.Menu(root,tearoff=0)
Popupmenu1.configure(background=colors['window'])
Popupmenu1.configure(fg=colors['text'])

fileM=tk.Menu(Popupmenu1,tearoff=0)
fileM.configure(background=colors['window'])
fileM.configure(fg=colors['text'])
Popupmenu1.add_cascade(menu=fileM,label='File')
fileM.add_command(command=NewFile,label='New',accelerator='Ctrl+N')
root.bind('<Control-n>',NewFile)
fileM.add_command(command=OpenFile,label='Open',accelerator='Ctrl+O')
root.bind('<Control-o>',OpenFile)
fileM.add_command(command=SaveFile,label='Save',accelerator='Ctrl+S')
root.bind('<Control-s>',SaveFile)
fileM.add_command(command=SaveAsFile,label='Save As')
fileM.add_separator()
fileM.add_command(command=Exit,label='Exit',accelerator='Ctrl+Q')
root.bind('<Control-q>',Exit)

import_export=tk.Menu(Popupmenu1,tearoff=0)
import_export.configure(background=colors['window'])
import_export.configure(fg=colors['text'])
Popupmenu1.add_cascade(menu=import_export,label='Import/Export')

importMenu=tk.Menu(import_export,tearoff=0)
importMenu.configure(background=colors['window'])
importMenu.configure(fg=colors['text'])
import_export.add_cascade(menu=importMenu,label='Import Objects')
importMenu.add_command(label='from APT',state=tk.DISABLED)
importMenu.add_command(label='from AstroPlanner',state=tk.DISABLED)
importMenu.add_command(label='from MaximDL',command=maximI)
importMenu.add_command(label='from SIPS',command=sipsI)

import_export.add_separator()
import_export.add_command(command=join,label='Join Files')

import_export.add_separator()
exportObj=tk.Menu(import_export,tearoff=0)
exportObj.configure(background=colors['window'])
exportObj.configure(fg=colors['text'])
import_export.add_cascade(menu=exportObj,label='Export Selected Objects',state=tk.DISABLED)
exportObj.add_command(label='to APT',command=aptE)
exportObj.add_command(label='to Excel',command=excelE)
exportObj.add_command(label='to MaximDL',command=maximE)
exportObj.add_command(label='to SIPS',command=sipsE)
exportObj.add_command(label='to Text File',command=textE)


exportObs=tk.Menu(import_export,tearoff=0)
exportObs.configure(background=colors['window'])
exportObs.configure(fg=colors['text'])
import_export.add_cascade(menu=exportObs,label='Export Observations of Object',state=tk.DISABLED)
exportObs.add_command(label='to Excel',command=excelObsE)
exportObs.add_command(label='to Text File',command=textObsE)

exportObsAll=tk.Menu(import_export,tearoff=0)
exportObsAll.configure(background=colors['window'])
exportObsAll.configure(fg=colors['text'])
import_export.add_cascade(menu=exportObsAll,label='Export All Observations',state=tk.DISABLED)
exportObsAll.add_command(label='to Excel',command=excelObsAllE)
exportObsAll.add_command(label='to Text File',command=textObsAllE)

Popupmenu1.add_command(command=Settings,label='Settings')
Popupmenu1.add_command(command=About,label='About')
root.config(menu=Popupmenu1)

obsFound=False
for o in objects.objects:
    if len(objects.objects[o]['obs'])>0:
        obsFound=True
        break
if obsFound: import_export.entryconfig('Export All Observations',state='normal')
else: import_export.entryconfig('Export All Observations',state='disabled')

NowTime()
objfilter()

if not os.path.isfile('data/settings.ops'):
    messagebox.showwarning('ObsPlanner','Please, configure your settings first!')
    Settings()

tk.mainloop()
