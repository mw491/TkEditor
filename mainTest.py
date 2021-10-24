import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *

from LineNumber import LineMain
from changefont import bold_it, italics_it, bg_color, all_text_color, text_color
# from findwindow import Finder
# from speak import SpeakMain
from syntax_highlight import SyntaxHighlight
from textarea import MyText

window = Tk()
window.title("Untitled - Python PyCode Tkeditor")
# window.attributes('-zoomed', True)
window.style = ttk.Style()
window.style.theme_use('clam')
window.minsize(670, 450)
window.iconphoto(False, PhotoImage(file="icon.png"))

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


def newfile(event=None):
    window.title("Untitled - Python PyCode TkEditor")
    textarea.delete(1.0, END)

    file_label["text"] = "Untitled.py"

    # reset undo and redo
    textarea.edit_reset()


def openfile(event=None):
    global file
    file = askopenfilename(filetypes=[("Python Files", "*.py"),
                                      ("All Files", "*.*"),
                                      ("Html Files", "*.html"),
                                      ("CSS Files", "*.css"),
                                      ("JavaScript Files", "*.js")])

    if file == "":
        file = None

    else:
        window.title(os.path.basename(file) + " - Python PyCode TkEditor")
        textarea.delete(1.0, END)
        openedfile = open(file, "r")
        textarea.insert(END, openedfile.read())
        openedfile.close()

    file_label["text"] = file

    # reset undo and redo
    textarea.edit_reset()


def savefile(event=None):
    global file
    if file == None:
        # save as new file
        file = asksaveasfilename(initialfile='Untitled',
                                 filetypes=[("Python Files", "*.py"),
                                            ("All Files", "*.*"),
                                            ("Html Files", "*.html"),
                                            ("CSS Files", "*.css"),
                                            ("JavaScript Files", "*.js")])

        if file == "":
            file = None
        else:
            window.title(os.path.basename(file) + " - Python PyCode TkEditor")
            savedfile = open(file, "w")
            savedfile.write(textarea.get(1.0, END))
            savedfile.close()
    else:
        savedfile = open(file, "w")
        savedfile.write(textarea.get(1.0, END))
        savedfile.close()

        file_label["text"] = os.path.basename(file)


def savefileas(event=None):
    global file
    file = asksaveasfilename(initialfile='Untitled',
                             filetypes=[("Python Files", "*.py"),
                                        ("All Files", "*.*"),
                                        ("Html Files", "*.html"),
                                        ("CSS Files", "*.css"),
                                        ("JavaScript Files", "*.js")])
    if file == "":
        file = None
    else:
        window.title(os.path.basename(file) + " - Python PyCode TkEditor")
        savedasfile = open(file, "w")
        savedasfile.write(textarea.get(1.0, END))
        savedasfile.close()

        file_label["text"] = file


def copy():
    textarea.event_generate("<<Copy>>")


def cut():
    textarea.event_generate("<<Cut>>")


def paste():
    textarea.event_generate("<<Paste>>")


def undo():
    textarea.event_generate("<<Undo>>")


def redo():
    textarea.event_generate("<<Redo>>")


def select_all(event=None):
    textarea.tag_add("sel", '1.0', 'end')


def deselect_all(event=None):
    textarea.tag_remove("sel", '1.0', 'end')


def speak(event=None):
    SpeakMain()


def showfindwindow(event=None):
    FindWindow(textarea)


def runfile(event=None):
    global file
    if file is None:
        save = showinfo("Save?", "You have to save your file before running,"
                                 " Are you sure you want to save now?",
                        type="okcancel")
        if save == "ok":
            file = asksaveasfilename(initialfile='Untitled',
                                     filetypes=[("Python Files", "*.py"),
                                                ("All Files", "*.*"),
                                                ("Html Files", "*.html"),
                                                ("CSS Files", "*.css"),
                                                ("JavaScript Files", "*.js")])
            if file == "":
                file = None
            else:
                window.title(os.path.basename(file) + " - Python PyCode TkEditor")
                savedasfile = open(file, "w")
                savedasfile.write(textarea.get(1.0, END))
                savedasfile.close()

                if keepconsole.get() == "yes":
                    os.system(f'gnome-terminal -- sh -c "python3 {file}; bash"')
                elif keepconsole.get() == "no":
                    os.system(f'gnome-terminal -- sh -c "python3 {file};"')

    else:
        savedfile = open(file, "w")
        savedfile.write(textarea.get(1.0, END))
        savedfile.close()

        file_label["text"] = os.path.basename(file)

        if keepconsole.get() == "yes":
            os.system(f'gnome-terminal -- sh -c "python3 {file}; bash"')
        elif keepconsole.get() == "no":
            os.system(f'gnome-terminal -- sh -c "python3 {file};"')


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


def show_hide_toolbar():
    if toggletoolbar.get() == "no":
        toolbar.pack_forget()
    elif toggletoolbar.get() == "yes":
        toolbar.pack(fill=X, side=TOP, before=textarea)


def showhelp(event=None):
    showinfo("Help", "my python editor made using python's tkinter module!")


def show_right_click_menu(event):
    right_click_menu.tk_popup(event.x_root, event.y_root)

    return


def autoindent(event=None):
    # the text widget that received the event
    widget = event.widget

    # get current line
    line = widget.get("insert linestart", "insert lineend")

    # compute the indentation of the current line
    match = re.match(r'^(\s+)', line)
    current_indent = len(match.group(0)) if match else 0

    # compute the new indentation
    new_indent = current_indent + 4

    # insert the character that triggered the event,
    # a newline, and then new indentation
    widget.insert("insert", event.char + "\n" + " " * new_indent)

    # return 'break' to prevent the default behavior
    return "break"


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


def update_wordnumber(event=None):
    lenth = len(textarea.get(1.0, END))
    current_wordnumber.set(f"Words: {lenth-1}")


file = None

toolbar = tk.Frame(window, bg="grey")
toolbar.pack(fill=X, side=TOP)

Button(toolbar, text="Copy", font=("Ubuntu Mono", 7), command=copy).grid(row=0, column=0, padx=2)
Button(toolbar, text="Cut", font=("Ubuntu Mono", 7), command=cut).grid(row=0, column=1, padx=2)
Button(toolbar, text="Paste", font=("Ubuntu Mono", 7), command=paste).grid(row=0, column=2, padx=2)
Button(toolbar, text="Run", font=("Ubuntu Mono", 7), command=runfile).grid(row=0, column=3, padx=2)
Button(toolbar, text="Undo", font=("Ubuntu Mono", 7), command=undo).grid(row=0, column=4, padx=2)
Button(toolbar, text="Redo", font=("Ubuntu Mono", 7),  command=redo).grid(row=0, column=5, padx=2)
Button(toolbar, text="Find", font=("Ubuntu Mono", 7),  command=showfindwindow).grid(row=0, column=6, padx=2)
Button(toolbar, text="Bold", font=("Ubuntu Mono", 7),
       command=lambda:bold_it(textarea)).grid(row=0, column=6, padx=2)
Button(toolbar, text="Italics", font=("Ubuntu Mono", 7),
       command=lambda:italics_it(textarea)).grid(row=0, column=7, padx=2)

status_bar = tk.Frame(window, bg="#404040", bd=2)
status_bar.pack(fill=X, side=BOTTOM)

current_index = StringVar()
index_label = Label(status_bar, textvar=current_index, font=(None, 8))
index_label.configure(foreground="white", background="#404040")
index_label.pack(side=RIGHT)


current_wordnumber = StringVar()
wordnumber_label = Label(status_bar, textvar=current_wordnumber, font=(None, 8))
wordnumber_label.configure(foreground="white", background="#404040")
wordnumber_label.pack(side=BOTTOM)


file_label = Label(status_bar, text="Untitled.py", font=(None, 8))
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
                   bg="#2b2b2b", fg="white", bd=1)

linenumbers = LineMain(textarea)

textarea.pack(fill=BOTH, expand=True)

topscrollbar.config(command=textarea.yview)
bottomscrollbar.config(command=textarea.xview)

SyntaxHighlight(textarea)

menubar = Menu(window, activebackground="#bfbfbf")
menubar.configure(bg="darkgrey", fg="black")
window.configure(menu=menubar)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=newfile, accelerator="Ctrl+N")
filemenu.add_command(label="Open", command=openfile, accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=savefile, accelerator="Ctrl+S")
filemenu.add_command(label="Save As", command=savefileas, accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_closing, accelerator="Ctrl+Q")

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
editmenu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
editmenu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
editmenu.add_separator()
editmenu.add_command(label="Find and Replace", command=showfindwindow,
                     accelerator="Ctrl+F")
editmenu.add_separator()
editmenu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", command=redo, accelerator="Ctrl+Shift+z")
editmenu.add_separator()
editmenu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
editmenu.add_command(label="Deselect All", command=deselect_all)
editmenu.add_separator()
editmenu.add_command(label="Bold Selected Text", command=lambda: bold_it(textarea),
                     accelerator="Ctrl+B")
editmenu.add_command(label="Italics Selected Text", command=lambda: italics_it(textarea),
                     accelerator="Ctrl+Shift+I")


runmenu = Menu(menubar, tearoff=0)
keepconsole = StringVar()
keepconsole.set("yes")
runmenu.add_command(label="Run File", command=runfile, accelerator="F5")
runmenu.add_checkbutton(label="Keep Console At Finnish", variable=keepconsole, onvalue="yes",
                        offvalue="no")

toolsmenu = Menu(menubar, tearoff=0)
themevar = StringVar()
themevar.set("classic")
toolsmenu.add_radiobutton(label="Toggle Classic Theme Recommended", variable=themevar,
                          value="classic",
                          command=classic_theme, accelerator="Alt+T")
toolsmenu.add_radiobutton(label="Toggle Light Theme", variable=themevar, value="light",
                          command=light_theme,
                          accelerator="Alt+L")
toolsmenu.add_radiobutton(label="Toggle Dark Theme", variable=themevar, value="dark",
                          command=dark_theme,
                          accelerator="Alt+D")
toolsmenu.add_separator()
toggletoolbar = StringVar()
toggletoolbar.set("yes")
toolsmenu.add_checkbutton(label="Show Toolbar", onvalue="yes", offvalue="no",
                          command=show_hide_toolbar, variable=toggletoolbar)
toolsmenu.add_separator()
toolsmenu.add_command(label="Change Selected Text Colour", command=lambda: text_color(textarea))
toolsmenu.add_command(label="Change Textarea Background Colour", command=lambda: bg_color(textarea))
toolsmenu.add_command(label="Change Textarea Foreground Colour", command=lambda: all_text_color(textarea))
toolsmenu.add_separator()
toolsmenu.add_command(label="Enter Text To Speak", command=speak, accelerator="Alt+S")

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=showhelp, accelerator="F1")

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="Run", menu=runmenu)
menubar.add_cascade(label="Tools", menu=toolsmenu)
menubar.add_cascade(label="Help", menu=helpmenu)

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
window.bind('<F5>', runfile)
window.bind("<Alt-t>", classic_theme)
window.bind("<Alt-l>", light_theme)
window.bind("<Alt-d>", dark_theme)
window.bind("<Alt-s>", speak)
window.bind("<F1>", showhelp)
window.bind('<Control-a>', select_all)
window.bind("<Control-q>", on_closing)
textarea.bind("<Button-2>", paste)
textarea.bind("<Button-3>", show_right_click_menu)
textarea.bind('<KeyRelease>', update_index)
textarea.bind("<KeyRelease>", update_wordnumber)
textarea.bind("<Control-b>", lambda event=None: bold_it(textarea))
textarea.bind("<Control-I>", lambda event=None: italics_it(textarea))

# textarea.bind(":", autoindent)

update_index()

window.mainloop()
#
#
# import tkinter as tk
# from tkinter import *
# from tkinter import ttk, filedialog
# import ttkthemes
#
# root = tk.Tk()
#
# fram = Frame(root)
# fram.pack(fill=BOTH, expand=True)
#
# canvas = Canvas(fram)
# canvas.pack(fill=BOTH, expand=1)
#
# sc = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
# sc.pack(fill=Y, side=RIGHT)
#
# canvas.configure(yscrollcommand=sc.set)
#
# canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
#
# fram2 = Frame(canvas)
# canvas.create_window((0, 0), window=fram2, anchor="nw")
#
# fram2.style = ttkthemes.ThemedStyle()
#
# for i, name in enumerate(sorted(fram2.style.theme_names())):
#     b = ttk.Button(fram2, text=name, command=lambda name=name:fram2.style.theme_use(name))
#     b.pack(fill="x")
#
#
# root.bind("<o>", lambda event=None:filedialog.askopenfilename())
#
# root.mainloop()

"""
22 September
"""




