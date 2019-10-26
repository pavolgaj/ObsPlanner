#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.14
# In conjunction with Tcl version 8.6
#    Oct 07, 2019 04:39:39 PM

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

import main_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    main_support.set_Tk_var()
    top = New_Toplevel (root)
    main_support.init(root, top)
    root.mainloop()

w = None
def create_New_Toplevel(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    main_support.set_Tk_var()
    top = New_Toplevel (w)
    main_support.init(w, top, *args, **kwargs)
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
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("834x451+418+179")
        top.title("New Toplevel")
        top.configure(highlightcolor="black")



        self.Scrolledlistbox1 = ScrolledListBox(top)
        self.Scrolledlistbox1.place(relx=0.02, rely=0.02, relheight=0.84
                , relwidth=0.32)
        self.Scrolledlistbox1.configure(background="white")
        self.Scrolledlistbox1.configure(font="TkFixedFont")
        self.Scrolledlistbox1.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox1.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox1.configure(width=10)
        self.Scrolledlistbox1.configure(listvariable=main_support.objs)
        
        for i in range(50):
            self.Scrolledlistbox1.insert(i,i+1)

        self.Scrolledlistbox2 = ScrolledListBox(top)
        self.Scrolledlistbox2.place(relx=0.36, rely=0.4, relheight=0.46
                , relwidth=0.27)
        self.Scrolledlistbox2.configure(background="white")
        self.Scrolledlistbox2.configure(font="TkFixedFont")
        self.Scrolledlistbox2.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox2.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox2.configure(width=10)
        self.Scrolledlistbox2.configure(listvariable=main_support.obss)
        
        for i in range(50):
            self.Scrolledlistbox2.insert(i,2*i)

        self.Canvas1 = Canvas(top)
        self.Canvas1.place(relx=0.66, rely=0.53, relheight=0.42, relwidth=0.32)
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(relief=RIDGE)
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(width=271)

        self.Canvas2 = Canvas(top)
        self.Canvas2.place(relx=0.66, rely=0.07, relheight=0.45, relwidth=0.32)
        self.Canvas2.configure(borderwidth="2")
        self.Canvas2.configure(relief=RIDGE)
        self.Canvas2.configure(selectbackground="#c4c4c4")
        self.Canvas2.configure(width=271)

        self.Entry1 = Entry(top)
        self.Entry1.place(relx=0.4, rely=0.04,height=23, relwidth=0.2)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="#c4c4c4")

        self.Button1 = Button(top)
        self.Button1.place(relx=0.61, rely=0.04, height=29, width=69)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Button''')

        self.Button2 = Button(top)
        self.Button2.place(relx=0.02, rely=0.91, height=29, width=69)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(text='''Button''')

        self.Button3 = Button(top)
        self.Button3.place(relx=0.13, rely=0.91, height=29, width=69)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(text='''Button''')

        self.Button4 = Button(top)
        self.Button4.place(relx=0.24, rely=0.91, height=29, width=69)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(text='''Button''')

        self.Button5 = Button(top)
        self.Button5.place(relx=0.36, rely=0.91, height=29, width=69)
        self.Button5.configure(activebackground="#d9d9d9")
        self.Button5.configure(text='''Button''')

        self.Text1 = Text(top)
        self.Text1.place(relx=0.37, rely=0.11, relheight=0.27, relwidth=0.25)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(width=206)
        self.Text1.configure(wrap=WORD)

    @staticmethod
    def popup1(event, *args, **kwargs):
        Popupmenu1 = Menu(root, tearoff=0)
        Popupmenu1.configure(activebackground="#f9f9f9")
        Popupmenu1.post(event.x_root, event.y_root)





# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

if __name__ == '__main__':
    vp_start_gui()


