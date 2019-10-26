#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.14
# In conjunction with Tcl version 8.6
#    Oct 07, 2019 06:38:07 PM

import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import object_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = New_Toplevel (root)
    object_support.init(root, top)
    root.mainloop()

w = None
def create_New_Toplevel(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = New_Toplevel (w)
    object_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_New_Toplevel():
    global w
    w.destroy()
    w = None


class New_Toplevel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 

        top.geometry("368x450+429+172")
        top.title("New Toplevel")
        top.configure(highlightcolor="black")



        self.Label1 = Label(top)
        self.Label1.place(relx=0.08, rely=0.07, height=21, width=43)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Name''')

        self.Entry1 = Entry(top)
        self.Entry1.place(relx=0.3, rely=0.07,height=23, relwidth=0.45)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="#c4c4c4")

        self.Label2 = Label(top)
        self.Label2.place(relx=0.14, rely=0.16, height=21, width=22)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''RA''')

        self.Entry2 = Entry(top)
        self.Entry2.place(relx=0.38, rely=0.18,height=23, relwidth=0.45)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="#c4c4c4")

        self.Button1 = Button(top)
        self.Button1.place(relx=0.6, rely=0.91, height=29, width=51)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Add''')

        self.Label3 = Label(top)
        self.Label3.place(relx=0.11, rely=0.24, height=21, width=31)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(text='''DEC''')

        self.Entry3 = Entry(top)
        self.Entry3.place(relx=0.35, rely=0.24,height=23, relwidth=0.45)
        self.Entry3.configure(background="white")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(selectbackground="#c4c4c4")

        self.Label4 = Label(top)
        self.Label4.place(relx=0.11, rely=0.4, height=21, width=32)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(text='''Mag''')

        self.Entry4 = Entry(top)
        self.Entry4.place(relx=0.35, rely=0.42,height=23, relwidth=0.45)
        self.Entry4.configure(background="white")
        self.Entry4.configure(font="TkFixedFont")
        self.Entry4.configure(selectbackground="#c4c4c4")

        self.Label5 = Label(top)
        self.Label5.place(relx=0.11, rely=0.53, height=21, width=31)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(text='''Size''')

        self.Entry5 = Entry(top)
        self.Entry5.place(relx=0.3, rely=0.53,height=23, relwidth=0.45)
        self.Entry5.configure(background="white")
        self.Entry5.configure(font="TkFixedFont")
        self.Entry5.configure(selectbackground="#c4c4c4")

        self.Label6 = Label(top)
        self.Label6.place(relx=0.14, rely=0.62, height=21, width=36)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(text='''Type''')

        self.Entry6 = Entry(top)
        self.Entry6.place(relx=0.33, rely=0.62,height=23, relwidth=0.45)
        self.Entry6.configure(background="white")
        self.Entry6.configure(font="TkFixedFont")
        self.Entry6.configure(selectbackground="#c4c4c4")

        self.Label7 = Label(top)
        self.Label7.place(relx=0.14, rely=0.71, height=21, width=42)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(text='''Notes''')

        self.Text1 = Text(top)
        self.Text1.place(relx=0.33, rely=0.71, relheight=0.16, relwidth=0.23)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(width=10)
        self.Text1.configure(wrap=WORD)

        self.Entry7 = Entry(top)
        self.Entry7.place(relx=0.38, rely=0.33,height=23, relwidth=0.29)
        self.Entry7.configure(background="white")
        self.Entry7.configure(font="TkFixedFont")
        self.Entry7.configure(width=106)

        self.Button2 = Button(top)
        self.Button2.place(relx=0.73, rely=0.33, height=29, width=69)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(text='''Detect''')

        self.Label8 = Label(top)
        self.Label8.place(relx=0.08, rely=0.33, height=21, width=90)
        self.Label8.configure(text='''Constellation''')






if __name__ == '__main__':
    vp_start_gui()


