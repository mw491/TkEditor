from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import *
import random


w = Tk()

width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

w.overrideredirect(1)

s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='#2F3333')
progress = Progressbar(w, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=550, mode='indeterminate')


#############progressbar          33333333333333333333333333333

def bar():
    progress.place(x=-10, y=235)
    l4 = Label(w, text='Loading...', fg='white', bg=a)
    lst4 = ('Calibri (Body)', 10)
    l4.config(font=lst4)
    l4.place(x=18, y=210)

    import time
    r = 0
    for i in range(30):
        progress['value'] = r
        w.update_idletasks()
        time.sleep(0.037)
        r = r + random.choice([8,9])

    w.destroy()
    from mainwindow import start




#############
# frame 333333333333333333333333
#
###########


'''

def rgb(r):
    return "#%02x%02x%02x" % r
#Frame(w,width=432,height=241,bg=rgb((100,100,100))).
'''
a = '#3C3F41'
Frame(w, width=427, height=241, bg=a).place(x=0, y=0)  # 249794
pic = PhotoImage(master=w, file="icon small.png")
######## Label

l1 = Label(w, text='TKEDITOR', fg='white', bg=a)
lst1 = ('Calibri (Body)', 18, 'bold')
l1.config(font=lst1)
l1.place(x=50, y=70)

l2 = Label(w, text='SIMPLE TEXT EDITOR', fg='white', bg=a)
lst2 = ('Calibri (Body)', 13)
l2.config(font=lst2)
l2.place(x=50, y=110)

l3 = Label(w, text='MADE WITH PYTHON', fg='white', bg=a)
lst3 = ('Calibri (Body)', 8)
l3.config(font=lst3)
l3.place(x=50, y=140)

l4 = Label(w, image=pic, bg=a)
l4.place(x=240, y=40)

# b1 = Button(w, width=10, height=2, text='START', command=bar, border=0, fg=a, bg='white')
# b1.config(font=lst3)
# b1.place(x=280, y=110)

w.after(1000, bar)

w.mainloop()


