import tkinter as tk
import tkinter.ttk as ttk 
import webbrowser
import sys
import os
import subprocess

def href(event):
    '''open hypertext href'''
    if sys.platform=='linux' or sys.platform=='linux2': 
        myEnv = dict(os.environ)
        lp_key = 'LD_LIBRARY_PATH'
        lp_orig = myEnv.get(lp_key + '_ORIG')
        if lp_orig is not None: myEnv[lp_key] = lp_orig
        else: lp = myEnv.get(lp_key)
        if lp is not None: myEnv.pop(lp_key)
        subprocess.call(['xdg-open',event.widget.cget("text")],env=myEnv)
    else: webbrowser.open_new(event.widget.cget("text"))

class fakeEvtWidget():
    '''generate event widget for "select" action'''
    def __init__(self,index,lst):
        self.index=index
        self.lst=list(lst)
    def curselection(self):
        return [self.index]
    def get(self,index):
        return self.lst[index]

class fakeEvt():
    '''generate event for "select" action'''
    def __init__(self,index,lst):
        self.widget=fakeEvtWidget(index,lst)

class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area=text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self,str):
        self.text_area.insert(tk.END,str)    

class AutoScroll(object):
    '''Configure the scrollbars for a widget.''' 
    def __init__(self,master):
        try: vsb=ttk.Scrollbar(master,orient='vertical',command=self.yview)
        except: pass
        hsb=ttk.Scrollbar(master,orient='horizontal',command=self.xview)

        try: self.configure(yscrollcommand=self._autoscroll(vsb))
        except: pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0,row=0,sticky='nsew')
        try: vsb.grid(column=1,row=0,sticky='ns')
        except: pass
        hsb.grid(column=0,row=1,sticky='ew')

        master.grid_columnconfigure(0,weight=1)
        master.grid_rowconfigure(0,weight=1)

        methods=tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() | tk.Place.__dict__.keys()
    
        for meth in methods:
            if meth[0] != '_' and meth not in ('config','configure'): setattr(self,meth,getattr(master,meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first,last):
            first,last=float(first),float(last)
            if first <= 0 and last >= 1: sbar.grid_remove()
            else: sbar.grid()
            sbar.set(first,last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master,and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls,master,**kw):
        container=ttk.Frame(master)
        return func(cls,container,**kw)
    return wrapped

class ScrolledListBox(AutoScroll,tk.Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self,master,**kw):
        tk.Listbox.__init__(self,master,**kw)
        AutoScroll.__init__(self,master)
        
class ScrolledText(AutoScroll,tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self,master,**kw):
        tk.Text.__init__(self,master,**kw)
        AutoScroll.__init__(self,master)
        
