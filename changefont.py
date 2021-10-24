from tkinter import *
from tkinter import colorchooser
from tkinter import font


# Bold Text
def bold_it(master):
    # Create our font
    bold_font = font.Font(master, master.cget("font"))
    bold_font.configure(weight="bold")

    # Configure a tag
    master.tag_configure("bold", font=bold_font)

    # will give TclError if nothing is selected
    try:
        # Define Current tags
        current_tags = master.tag_names("sel.first")
        # If statment to see if tag has been set
        if "bold" in current_tags:
            master.tag_remove("bold", "sel.first", "sel.last")
        else:
            master.tag_add("bold", "sel.first", "sel.last")

    except TclError:
        pass

# Italics Text
def italics_it(master):
    # Create our font
    italics_font = font.Font(master, master.cget("font"))
    italics_font.configure(slant="italic")

    # Configure a tag
    master.tag_configure("italic", font=italics_font)

    # will give TclError if nothing is selected
    try:
        # Define Current tags
        current_tags = master.tag_names("sel.first")

        # If statment to see if tag has been set
        if "italic" in current_tags:
            master.tag_remove("italic", "sel.first", "sel.last")
        else:
            master.tag_add("italic", "sel.first", "sel.last")
    except TclError:
        pass


# Change Selected Text Color
def text_color(master):
    # Pick a color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        # Create our font
        color_font = font.Font(master, master.cget("font"))

        # Configure a tag
        master.tag_configure("colored", font=color_font, foreground=my_color)

        # Define Current tags
        current_tags = master.tag_names("sel.first")

        # If statment to see if tag has been set
        if "colored" in current_tags:
            master.tag_remove("colored", "sel.first", "sel.last")
        else:
            master.tag_add("colored", "sel.first", "sel.last")


# Change bg color
def bg_color(master):
    my_color = colorchooser.askcolor()[1]
    if my_color:
        master.config(bg=my_color)


# Change ALL Text Color
def all_text_color(master):
    my_color = colorchooser.askcolor()[1]
    if my_color:
        master.config(fg=my_color)


if __name__ == '__main__':
    w=Tk()
    t=Text()
    t.pack()
    t.bind("<Control-b>", lambda e: bold_it(t))

    w.mainloop()
