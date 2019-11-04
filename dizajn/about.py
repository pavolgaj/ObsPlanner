import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from PIL import ImageTk, Image

def href(event):
    webbrowser.open_new(event.widget.cget("text"))

top=tk.Tk()

top.geometry('310x240')
top.title('About')
top.resizable(False,False)

img=Image.open('ObsPlanner.png')
img=img.resize((80,80),Image.ANTIALIAS)
img=ImageTk.PhotoImage(img)
LabelImg=tk.Label(top)
LabelImg.place(relx=0.37,rely=0.04,height=80,width=80)
LabelImg.configure(image=img)

Label1=tk.Label(top)
Label1.place(relx=0.0,rely=0.4,height=27,width=310)
Label1.configure(font='-family {DejaVu Sans} -size 14 -weight bold -slant roman -underline 0 -overstrike 0')
Label1.configure(text='ObsPlanner')

Label3=tk.Label(top)
Label3.place(relx=0.0,rely=0.52,height=21,width=310)
Label3.configure(text='version 0.1')

Label4=tk.Label(top)
Label4.place(relx=0.0,rely=0.64,height=21,width=310)
Label4.configure(font='-family {DejaVu Sans} -size 10 -weight normal -slant roman -underline 1 -overstrike 0')
Label4.configure(foreground='blue')
Label4.configure(cursor='hand2')
Label4.configure(text='http://pavolg.6f.sk')
Label4.bind('<Button-1>',href)

Label4_1=tk.Label(top)
Label4_1.place(relx=0.0,rely=0.76,height=21,width=310)
Label4_1.configure(font='-family {DejaVu Sans} -size 10 -weight normal -slant roman -underline 1 -overstrike 0')
Label4_1.configure(foreground='blue')
Label4_1.configure(cursor='hand2')
Label4_1.configure(text='https://github.com/pavolgaj/ObsPlanner')
Label4_1.bind('<Button-1>',href)

Label2=tk.Label(top)
Label2.place(relx=0.0,rely=0.88,height=21,width=310)
Label2.configure(text='(c) Pavol Gajdoš,2019')

tk.mainloop()



