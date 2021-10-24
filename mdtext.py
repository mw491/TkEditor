# import flask, markdown
#
# app = flask.Flask(__name__)
#
# file = "# hello"
#
# @app.route("/")
# def display_md():
#     return markdown.markdown(file.read())
#
#
# if __name__ == '__main__':
#     app.run(host="127.0.0.1")


# from tkinter import *
# from tkinter.filedialog import*
# from tkinter.messagebox import *
# from flask import Flask
# import markdown, pyflatpak, linenumbering
#
# from findwindow import Finder
#
# # main window
# window = Tk(className="MDText")
# window.title("Untitled | MDText")
# window.attributes("-zoomed", True)
#
# # functions
# def newfile(event=None):
#     window.title("Untitled - Python PyCode TkEditor")
#     textarea.delete(1.0, END)
#     # reset undo and redo
#     textarea.edit_reset()
#
#
# def openfile(event=None):
#     global file
#     file = askopenfilename(filetypes=[("Markdown Files Files", "*.md"),
#                                       ("All Files", "*.*"),
#                                       ("Text Files", "*.txt")])
#
#     if file == "":
#         file = None
#
#     else:
#         window.title(os.path.basename(file) + " | MDText")
#         textarea.delete(1.0, END)
#         openedfile = open(file, "r")
#         try:
#             textarea.insert(END, openedfile.read())
#         except UnicodeDecodeError as error:
#             showerror("Unicode Error!", error)
#         openedfile.close()
#
#     # reset undo and redo
#     textarea.edit_reset()
#
#
# def savefile(event=None):
#     global file
#     if file == None:
#         # save as new file
#         file = asksaveasfilename(initialfile='Untitled',
#                                  filetypes=[("Markdown Files", "*.md"),
#                                             ("All Files", "*.*")])
#
#         if file == "":
#             file = None
#         else:
#             window.title(os.path.basename(file) + " - MDText")
#             savedfile = open(file, "w")
#             savedfile.write(textarea.get(1.0, END))
#             savedfile.close()
#     else:
#         savedfile = open(file, "w")
#         savedfile.write(textarea.get(1.0, END))
#         savedfile.close()
#
#
# def savefileas(event=None):
#     global file
#     file = asksaveasfilename(initialfile='Untitled',
#                              filetypes=[("Markdown Files", "*.md"),
#                                         ("All Files", "*.*")])
#     if file == "":
#         file = None
#     else:
#         window.title(os.path.basename(file) + " - Python PyCode TkEditor")
#         savedasfile = open(file, "w")
#         savedasfile.write(textarea.get(1.0, END))
#         savedasfile.close()
#
#
# def copy():
#     textarea.event_generate("<<Copy>>")
#
#
# def cut():
#     textarea.event_generate("<<Cut>>")
#
#
# def paste():
#     textarea.event_generate("<<Paste>>")
#
#
# def undo():
#     textarea.event_generate("<<Undo>>")
#
#
# def redo():
#     textarea.event_generate("<<Redo>>")
#
#
# def select_all(event=None):
#     # textarea.tag_add("sel", '1.0', 'end')
#     textarea.event_generate("<<SelectAll>>")
#
#
# def deselect_all(event=None):
#     textarea.tag_remove("sel", '1.0', 'end')
#
#
# def showfindwindow(event=None):
#     Finder(window, textarea).pack(fill=X)
#
#
# def show_right_click_menu(event):
#     right_click_menu.tk_popup(event.x_root, event.y_root)
#
#     return
#
#
# textarea = Text(window)
# linenumbering.Linenumbers(textarea)
# textarea.pack(fill=BOTH, expand=True)
#
# menubar = Menu(window)
# window.configure(menu=menubar)
#
# filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=newfile, accelerator="Ctrl+N")
# filemenu.add_command(label="Open", command=openfile, accelerator="Ctrl+O")
# filemenu.add_command(label="Save", command=savefile, accelerator="Ctrl+S")
# filemenu.add_command(label="Save As", command=savefileas, accelerator="Ctrl+Shift+S")
# filemenu.add_separator()
# filemenu.add_command(label="Exit", command=window.destroy, accelerator="Ctrl+Q")
#
# editmenu = Menu(menubar, tearoff=0)
# editmenu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
# editmenu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
# editmenu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
# editmenu.add_separator()
# editmenu.add_command(label="Find and Replace", command=showfindwindow,
#                      accelerator="Ctrl+F")
# editmenu.add_separator()
# editmenu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
# editmenu.add_command(label="Redo", command=redo, accelerator="Ctrl+Shift+z")
# editmenu.add_separator()
# editmenu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
# editmenu.add_command(label="Deselect All", command=deselect_all)
#
# helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="About", command=lambda: showinfo("About", "MDText, Markdown Editor"))
#
# menubar.add_cascade(label="File", menu=filemenu)
# menubar.add_cascade(label="Edit", menu=editmenu)
# menubar.add_cascade(label="Help", menu=helpmenu)
#
# right_click_menu = Menu(textarea, tearoff=0)
# right_click_menu.add_command(label='Copy', command=copy)
# right_click_menu.add_command(label='Cut', command=cut)
# right_click_menu.add_command(label='Paste', command=paste)
# right_click_menu.add_separator()
# right_click_menu.add_command(label="Undo", command=undo)
# right_click_menu.add_command(label="Redo", command=redo)
# right_click_menu.add_separator()
# right_click_menu.add_command(label="Select All", command=select_all)
# right_click_menu.add_command(label="Deselect All", command=deselect_all)
#
# window.bind("<Control-o>", openfile)
# window.bind("<Control-s>", savefile)
# window.bind('<Control-S>', savefileas)
# window.bind("<Control-f>", showfindwindow)
# window.bind('<Control-a>', select_all)
#
# textarea.bind("<Button-2>", paste)
# textarea.bind("<Button-3>", show_right_click_menu)
#
# window.mainloop()

from tkinter import *
import pkinter as pk
from tkinter import ttk
import tkinter as tk
import time
import os

def write_text(text_to_print):
    text.insert(INSERT, text_to_print)

def load():
    text.delete('1.0', END)
    filename = os.path.join(fileDir, 'PowerWordProjects/' + fileloadentry.get() + '')
    filecontent = open(filename, "r")
    filecontent = filecontent.read()
    write_text(filecontent)
    print(filename)

def save():
    newfilecontent = text.get("1.0",'end-1c')
    print(newfilecontent)
    newfilepath = 'PowerWordProjects/'
    newfilename = os.path.join(newfilepath, savenameentry.get())
    newfile = open(newfilename, 'w+')
    newfile.write(newfilecontent)
    newfile.close()
    write_text("\nSaved to PowerWordProjects.")

def clear():
    text.delete('1.0', END)

fileDir = os.path.dirname(os.path.realpath('__file__'))
print(fileDir)

# Main window
root = Tk()
root.wm_title("PowerWord")


creditlabel = Label(root,
                    #text = 'An open source text editor, made by ShinyMemesYT.',
                    text = 'An open source code editor, and plain text editor in the one app.',
                    font = ('Ariel',15))

creditlabel.pack()

loadlabel = Label(root,
                    text = 'Load',
                  font = ('Ariel',30))

loadlabel.pack()

fileloadentry = Entry(root)
fileloadentry.pack()

text = Text(root, height=18)
scrollbar = ttk.Scrollbar(root)
linenumbers = pk.LineNumbers(root, text, scrollbar)

write_text("Empty text file. Clear this then you can write your own text then save it!")

loadbutton = Button(root, text="Load", width=10, height=1, command=load)

loadbutton.pack()

newlabel = Label(root,
                   text = 'New',
                   font = ('Ariel',30))

newlabel.pack()

savenamelabel = Label(root, text="Name for the new file(remember the extension):")
savenamelabel.pack()

savenameentry = Entry(root)
savenameentry.pack()

savebutton = Button(root, width=20, height=1, text="Save", command=save)

savebutton.pack()

clearbutton = Button(root, text="Clear", width=20, height=1, command=clear)

clearbutton.pack()

linenumbers.pack(side="left", fill="y")
scrollbar.pack(side="right", fill="y")
text.pack(side="right", fill="both")

root.mainloop()


'''
&#169;
'''
