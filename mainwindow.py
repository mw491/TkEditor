import pathlib
import tkinter as tk
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import Tklighter

from show_help import HelpWindow
from LineNumber import LineMain
from textarea import MyText
from findwindow import Finder
from configparser import ConfigParser
from changefont import bg_color, all_text_color
import ctypes

myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


# window = ThemedTk(theme="adapdta")
window = Tk()
window.title("Untitled - TkEditor")
window.minsize(670, 450)
window.iconphoto(False, PhotoImage(file="icon.png"))

window.tk.call("source", "C:/Users/MW/Desktop/programs/text editor/text editor/sun-valley.tcl")
window.tk.call("set_theme", "light")

themevar = StringVar()


# hide hidden files in filedialog
try:
    try:
        window.tk.call('tk_getOpenFile', '-foobarbaz')
    except TclError:
        pass
    # now set the magic variables accordingly
    window.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
    window.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
except TclError:
    pass

class MenuBar(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bd=1, relief='raised')
        self.master = master
        self.config(background="#3C3F41")

        file_b = tk.Menubutton(self, text="File", background="#3C3F41", foreground="white", activebackground="#3C3F41", activeforeground="white")
        filemenu = tk.Menu(file_b, tearoff=0)

        filemenu.add_command(label="New", command=newfile, accelerator="Ctrl+N", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        filemenu.add_command(label="Open", command=openfile, accelerator="Ctrl+O", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        filemenu.add_command(label="Save", command=savefile, accelerator="Ctrl+S", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        filemenu.add_command(label="Save As", command=savefileas, accelerator="Ctrl+Shift+S", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        filemenu.add_separator(background="#3C3F41")
        filemenu.add_command(label="Exit", command=on_closing, accelerator="Ctrl+Q", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")

        file_b.config(menu=filemenu)
        file_b["borderwidth"] = 0
        file_b.pack(side='left', pady=5, padx=3)

        edit_b = tk.Menubutton(self, text="Edit", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        editmenu = tk.Menu(edit_b, tearoff=0)
        editmenu.add_command(label="Copy", command=copy, accelerator="Ctrl+C", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        editmenu.add_command(label="Cut", command=cut, accelerator="Ctrl+X", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        editmenu.add_command(label="Paste", command=paste, accelerator="Ctrl+V", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        editmenu.add_separator(background="#3C3F41")
        editmenu.add_command(label="Find and Replace", command=showfindwindow,
                             accelerator="Ctrl+F", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        editmenu.add_separator(background="#3C3F41")
        editmenu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        editmenu.add_command(label="Redo", command=redo, accelerator="Ctrl+Shift+z", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        editmenu.add_separator(background="#3C3F41")
        editmenu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        editmenu.add_command(label="Deselect All", command=deselect_all, background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")

        edit_b.config(menu=editmenu)
        edit_b["borderwidth"] = 0
        edit_b.pack(side='left', pady=5, padx=3)

        toolsmenu_b = tk.Menubutton(self, text="Tools", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        toolsmenu = tk.Menu(toolsmenu_b, tearoff=0)
        themevar = StringVar()
        themevar.set("classic")
        toolsmenu.add_radiobutton(label="Toggle Classic Theme Recommended", variable=themevar,
                                  value="classic",
                                  command=classic_theme, accelerator="Alt+T", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        toolsmenu.add_radiobutton(label="Toggle Light Theme", variable=themevar, value="light",
                                  command=light_theme,
                                  accelerator="Alt+L", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        toolsmenu.add_radiobutton(label="Toggle Dark Theme", variable=themevar, value="dark",
                                  command=dark_theme,
                                  accelerator="Alt+D", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        toolsmenu.add_separator(background="#3C3F41")
        toolsmenu.add_command(label="Change Textarea Background Colour", command=lambda: bg_color(textarea), background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        toolsmenu.add_command(label="Change Textarea Foreground Colour", command=lambda: all_text_color(textarea), background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")

        toolsmenu_b.config(menu=toolsmenu)
        toolsmenu_b["borderwidth"] = 0
        toolsmenu_b.pack(side='left', pady=5, padx=3)

        helpmenu_b = tk.Menubutton(self, text="About", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")
        helpmenu = tk.Menu(helpmenu_b, tearoff=0)
        helpmenu.add_command(label="About", command=showhelp, accelerator="F1", background="#3C3F41", foreground="white", activebackground="#2F3333", activeforeground="white")

        helpmenu_b.config(menu=helpmenu)
        helpmenu_b["borderwidth"] = 0
        helpmenu_b.pack(side="left", pady=(5,2), padx=1)

        text = tk.Label(self, text=file, foreground="gray", background="#3C3F41", padx=20)
        text.pack(side="left")

        close = tk.Button(self, text='X', command=lambda: window.destroy(),
                          background='#262626',
                          foreground='white',
                          activebackground="red", width="6", height=2, bd=0)
        close.pack(side='right')
        def hover(event=None):
            close["background"] = "#C10D1C"
        def nothover(event=None):
            close["background"] = "#262626"
        close.bind("<Enter>", hover)
        close.bind("<Leave>", nothover)


# def changetheme(theme):




def newfile(event=None):
    window.title("Untitled - TkEditor")
    textarea.delete(1.0, END)

    file_label["text"] = "Untitled.txt"
    update_index()
    # reset undo and redo
    textarea.edit_reset()


def openfile(event=None):
    global file
    file = askopenfilename(initialdir=os.path.expanduser('~user'),
                           filetypes=[("All Files", "*.*"),
                                      ("Text Files", "*.txt")])

    if file == "":
        file = None

    else:
        window.title(os.path.basename(file) + " - TkEditor")
        textarea.delete(1.0, END)
        openedfile = open(file, "r")
        try:
            textarea.insert(END, openedfile.read())
        except UnicodeDecodeError as error:
            showerror("Unicode Error!", error)
        openedfile.close()

    file_label["text"] = file

    # reset undo and redo
    textarea.edit_reset()
    update_index()


def savefile(event=None):
    global file
    if file == None:
        # save as new file
        file = asksaveasfilename(initialfile='Untitled',
                                 filetypes=[("All Files", "*.*"),
                                            ("Text File", "*.txt"),])

        if file == "":
            file = None
        else:
            window.title(os.path.basename(file) + " - TkEditor")
            savedfile = open(file, "w")
            savedfile.write(textarea.get(1.0, END))
            savedfile.close()
    else:
        savedfile = open(file, "w")
        savedfile.write(textarea.get(1.0, END))
        savedfile.close()

        file_label["text"] = os.path.basename(file)
        update_index()


def savefileas(event=None):
    global file
    file = asksaveasfilename(initialfile='Untitled',
                             filetypes=[("All Files", "*.*"),
                                        ("Text Files", "*.txt")])
    if file == "":
        file = None
    else:
        window.title(os.path.basename(file) + " - TkEditor")
        savedasfile = open(file, "w")
        savedasfile.write(textarea.get(1.0, END))
        savedasfile.close()

        file_label["text"] = file
        update_index()


def copy():
    textarea.event_generate("<<Copy>>")


def cut():
    textarea.event_generate("<<Cut>>")
    update_index()


def paste():
    textarea.event_generate("<<Paste>>")
    update_index()


def undo():
    textarea.event_generate("<<Undo>>")
    update_index()


def redo():
    textarea.event_generate("<<Redo>>")
    update_index()


def select_all(event=None):
    # textarea.tag_add("sel", '1.0', 'end')
    textarea.event_generate("<<SelectAll>>")


def deselect_all(event=None):
    textarea.tag_remove("sel", '1.0', 'end')


def showfindwindow(event=None):
    f = Finder(window, textarea, bg="#262626", height=3)
    f.pack(fill="x")


def light_theme(event=None):
    textarea.configure(insertbackground='black', bg="white", fg="black")
    menubar.configure(bg="lightgrey", fg="black")
    themevar.set("light")


def dark_theme(event=None):
    textarea.configure(insertbackground='white', bg="#232342", fg="white")
    menubar.configure(bg="lightgrey", fg="black")
    themevar.set("dark")


def classic_theme(event=None):
    textarea.configure(insertbackground='white', bg="#2b2b2b", fg="white")
    menubar.configure(bg="darkgrey", fg="black")
    themevar.set("classic")


def showhelp(event=None):
    # showinfo("Help", "my python editor made using python's tkinter module!")
    HelpWindow()


def show_right_click_menu(event):
    right_click_menu.tk_popup(event.x_root, event.y_root)

    return



def tab(event=None):
    textarea.insert(INSERT, "   ")
    return 'break'


def on_closing(event=None):
    leave = showwarning("Exit?", "Are you sure you want to quit?", type="yesno")
    if leave == "yes":
        window.destroy()
    else:
        pass
window.protocol("WM_DELETE_WINDOW", on_closing)


def update_index(event=None):
    cursor_position = textarea.index(INSERT)
    cursor_position_pieces = str(cursor_position).split('.')

    cursor_line = cursor_position_pieces[0]
    cursor_column = cursor_position_pieces[1]

    current_index.set(f'Ln: {cursor_line}, Col: {cursor_column}')


file = None

menubar = MenuBar(window)
menubar.pack(side='top', fill='x')
#
#
# menubar.bind("<Button-1>", startMove)
# menubar.bind("<ButtonRelease-1>", stopMove)
# menubar.bind("<B1-Motion>", moving)

status_bar = tk.Frame(window, bg="#404040", bd=2)
status_bar.pack(fill=X, side=BOTTOM)

current_index = StringVar()
index_label = Label(status_bar, textvar=current_index, font=(None, 8))
index_label.configure(foreground="white", background="#404040")
index_label.pack(side=RIGHT)

file_label = Label(status_bar, text="Untitled.txt", font=(None, 8))
file_label.configure(foreground="white", background="#404040")
file_label.pack(side=LEFT)

topscrollbar = ttk.Scrollbar(window)
topscrollbar.pack(fill=Y, side=RIGHT)

bottomscrollbar = ttk.Scrollbar(window, orient='horizontal')
bottomscrollbar.pack(fill=X, side=BOTTOM)

textarea = MyText(window, font=("Ubuntu Mono", 14), undo=True, yscrollcommand=topscrollbar.set,
                  xscrollcommand=bottomscrollbar.set)
textarea.configure(wrap=NONE, insertbackground="white", selectforeground="white",
                   selectbackground="#595959",
                   bg="#2b2b2b", fg="white")

TKlighter.def_h(textarea,"#ff0000")

linenumbers = LineMain(textarea)

textarea.pack(fill=BOTH, expand=True)
textarea.focus_set()

topscrollbar.config(command=textarea.yview)
bottomscrollbar.config(command=textarea.xview)

# menubar = Menu(window, activebackground="#bfbfbf")
# menubar.configure(bg="darkgrey", fg="black")
# window.configure(menu=menubar)
#
# filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=newfile, accelerator="Ctrl+N")
# filemenu.add_command(label="Open", command=openfile, accelerator="Ctrl+O")
# filemenu.add_command(label="Save", command=savefile, accelerator="Ctrl+S")
# filemenu.add_command(label="Save As", command=savefileas, accelerator="Ctrl+Shift+S")
# filemenu.add_separator()
# filemenu.add_command(label="Exit", command=on_closing, accelerator="Ctrl+Q")
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
# editmenu.add_separator()
#
# toolsmenu = Menu(menubar, tearoff=0)
# themevar = StringVar()
# themevar.set("classic")
# toolsmenu.add_radiobutton(label="Toggle Classic Theme Recommended", variable=themevar,
#                           value="classic",
#                           command=classic_theme, accelerator="Alt+T")
# toolsmenu.add_radiobutton(label="Toggle Light Theme", variable=themevar, value="light",
#                           command=light_theme,
#                           accelerator="Alt+L")
# toolsmenu.add_radiobutton(label="Toggle Dark Theme", variable=themevar, value="dark",
#                           command=dark_theme,
#                           accelerator="Alt+D")
# toolsmenu.add_separator()
# toolsmenu.add_command(label="Change Textarea Background Colour", command=lambda: bg_color(textarea))
# toolsmenu.add_command(label="Change Textarea Foreground Colour", command=lambda: all_text_color(textarea))
# toolsmenu.add_separator()
#
# helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="About", command=showhelp, accelerator="F1")
#
# menubar.add_cascade(label="File", menu=filemenu)
# menubar.add_cascade(label="Edit", menu=editmenu)
# menubar.add_cascade(label="Tools", menu=toolsmenu)
# menubar.add_cascade(label="Help", menu=helpmenu)

right_click_menu = Menu(textarea, tearoff=0)
right_click_menu.add_command(label='Copy', command=copy)
right_click_menu.add_command(label='Cut', command=cut)
right_click_menu.add_command(label='Paste', command=paste)
right_click_menu.add_separator()
right_click_menu.add_command(label="Undo", command=undo)
right_click_menu.add_command(label="Redo", command=redo)
right_click_menu.add_separator()
right_click_menu.add_command(label="Select All", command=select_all)
right_click_menu.add_command(label="Deselect All", command=deselect_all)


window.bind("<Control-n>", newfile)
window.bind("<Control-o>", openfile)
window.bind("<Control-s>", savefile)
window.bind('<Control-S>', savefileas)
window.bind("<Control-f>", showfindwindow)
window.bind("<Alt-t>", classic_theme)
window.bind("<Alt-l>", light_theme)
window.bind("<Alt-d>", dark_theme)
window.bind("<F1>", showhelp)
window.bind('<Control-a>', select_all)
window.bind("<Control-q>", on_closing)
textarea.bind("<Button-2>", paste)
textarea.bind("<Button-3>", show_right_click_menu)
textarea.bind('<KeyRelease>', update_index)
textarea.bind("<Tab>", tab)
textarea.bind("<<ContentChanged>>", update_index)

update_index()

def start():
    window.mainloop()


if __name__ == '__main__':
    window.mainloop()
