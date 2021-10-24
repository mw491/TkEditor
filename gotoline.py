from tkinter import simpledialog
from tkinter import *


class GotoLine:
    def __init__(self, textwidget: Text):
        self.textwidget = textwidget
        self.lineno = simpledialog.askinteger(
            "Go to Line", "Type a line number and press Enter:",
            parent=self.textwidget.winfo_toplevel())
        if self.lineno is not None:  # not cancelled
            # there's no need to do a bounds check because tk ignores out-of-bounds
            # text indexes
            self.column = self.textwidget.index('insert').split('.')[0]
            self.textwidget.mark_set('insert', '%d.%s' % (self.lineno, self.column))
            self.textwidget.see('insert')

        self.textwidget.focus_set()


if __name__ == '__main__':
    w=Tk()
    t=Text()
    t.pack()
    t.insert(END, "sdfdfsf\nasdfsdfsd\nsdfasdf\n")
    t.bind("<Control-l>", lambda e:GotoLine(t))
    w.mainloop()