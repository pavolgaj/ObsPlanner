#!/usr/bin/python3
import sys
import os

from tkinter import *
from tkinter import messagebox  
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
    return sorted(list(zoznam))    

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
        else: name=nameVar.get()
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
        if obj is None: objects.add(nameVar.get(),ra,dec,magVar.get(),sizeVar.get(),typeVar.get(),note,constVar.get())    
        else: objects.objects[obj.name]['object']=stars.star(nameVar.get(),ra,dec,magVar.get(),sizeVar.get(),typeVar.get(),note,constVar.get())
        
        objfilter()
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

def AddObs():
    print('AddObs')
    sys.stdout.flush()

def DelObj():
    print('DelObj')
    sys.stdout.flush()

def DelObs():
    print('DelObs')
    sys.stdout.flush()

def EditObj():
    AddObj(objZ)
    fake=fakeEvt()
    objselect(fake)

def EditObs():
    print('EditObs')
    sys.stdout.flush()

def Exit(): 
    global root
    root.destroy()
    root=None
    matplotlib.pyplot.close()

def NewFile():
    print('NewFile')
    sys.stdout.flush()

def NowTime():
    dt=datetime.datetime.now(datetime.timezone.utc)
    dateVar.set(dt.strftime('%Y-%m-%d %H:%M:%S'))

def OpenFile():
    print('OpenFile')
    sys.stdout.flush()

def SaveFile():
    print('SaveFile')
    sys.stdout.flush()

def Settings():
    print('Settings')
    sys.stdout.flush()

def ShowImg():
    print('ShowImg')
    sys.stdout.flush()
    
def getDate():
    try: dt=datetime.datetime.strptime(dateVar.get(),'%Y-%m-%d %H:%M:%S')
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
    rect=patches.Rectangle((limits[2],limits[0]),limits[3]-limits[2],limits[1]-limits[0],linewidth=1,edgecolor='gray',facecolor='white')
    ax.add_patch(rect)
    
    year,mon,day,hour,minute,sec=getDate()
    jd0=stars.juldat(year,mon,day,hour-2,minute,sec)  #start -2h
    jd1=stars.juldat(year,mon,day,hour+12,minute,sec)  #stop 12h
    jd=np.linspace(jd0,jd1,200)
    
    a,h=objZ.altAz(jd,lon,lat)
    h0=h[np.where(h>0)]
    a0=a[np.where(h>0)]
    ax.plot(a0,h0,'k-')
    ax.set_xlim(min(a0)-5,max(a0)+5)
    ax.set_ylim(min(h0),max(h)+5) 
    
    #znacky po hodinach
    jdH=np.arange(stars.juldat(year,mon,day,hour-1,0,0),stars.juldat(year,mon,day,hour+13,0,1),1./24.)
    for i in range(len(jdH)):
        a,h=objZ.altAz(jdH[i],lon,lat)
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
    a,h=objZ.altAz(jd,lon,lat)
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
            a,h=ob['object'].altAz(jd,lon,lat)
            if (a<limits[3]) and (a>limits[2]) and (h<limits[1]) and (h>limits[0]): 
                zoznam.append(ob['object'].name)
    elif filt=='Above horizont': 
        year,mon,day,hour,minute,sec=getDate()
        jd=stars.juldat(year,mon,day,hour,minute,sec)
        for ob in objects.objects.values():
            a,h=ob['object'].altAz(jd,lon,lat)
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
                a,h=ob['object'].altAz(jd,lon,lat)
                if (a<limits[3]) and (a>limits[2]) and (h<limits[1]) and (h>limits[0]): 
                    zoznam.append(ob['object'].name)
    objsVar.set(sort(zoznam))     
    
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
    a,h=objZ.altAz(stars.juldat(year,mon,day,hour,minute,sec),lon,lat)
    print('Az: '+stars.printDMS(a)+'; Alt: '+stars.printDMS(h))
    r,t,s=objZ.rise(stars.juldat(year,mon,day+round(hour/24.),0,0,0),lon,lat)
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
    print('Site: '+obsZ1.site) 
    print('---------------------')
    print('Note: '+obsZ1.note)    
    sys.stdout=old 

constellations=stars.load()
objects=objClass.objects(constellations)

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

Button3=Button(Labelframe0)
Button3.place(relx=0.65,rely=0.95,height=24,width=47) 
Button3.configure(command=DelObj)
Button3.configure(text='Delete')

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

Button5=Button(Labelframe1)
Button5.place(relx=0.28,rely=0.95,height=24,width=47)   
Button5.configure(command=EditObs)
Button5.configure(text='Edit')

Button6=Button(Labelframe1)
Button6.place(relx=0.53,rely=0.95,height=24,width=47)   
Button6.configure(command=DelObs)
Button6.configure(text='Delete')

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

#z nastaveni
#suradnice
lat=49
lon=21.25    
limits=[5,40,190,330]   #min_alt,max_alt,min_az,max_az

NowTime()
objfilter()

mainloop()
