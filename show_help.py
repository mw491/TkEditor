from tkinter import *
from tkinter import ttk
from platform import uname


class HelpWindow(Toplevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # # # # # # Window Options # # # # # # #
        # Transient
        self.transient(self.master)
        # Title
        self.title("About TkEditor")
        # Geometry, windows default size
        self.geometry("380x580+30+50")

        # self.tk.call("source", "C:/Users/MW/Desktop/programs/text editor/text editor/sun-valley.tcl")
        # self.tk.call("set_theme", "light")

        # Disable Resizing
        # self.resizable(0, 0)

        # # # # # # Main Frame # # # # # # #
        self.main_frame = Frame(self, bd=4, bg="#bbbbbb", relief=GROOVE)
        self.main_frame.pack(fill=BOTH, expand=True, pady=5, padx=10)

        pic = PhotoImage(master=self, file="icon small.png")

        # # # # # # Main Items # # # # # # #

        # # # # # # Labels # # # # # # #
        Label(self.main_frame, image=pic, text="    TkEditor", bg="#bbbbbb",
              compound=LEFT, font=("Monospace", 15, "bold")).pack(pady=15, padx=10)

        Label(self.main_frame, text="My Python Editor,\nA simple python Editor.\nMade in Python3! And Tkinter",
              bg="#bbbbbb", font=("Ubuntu Mono", 13)).pack(pady=8, padx=13)

        Label(self.main_frame, text="Email: musaiw@outlook.com", bg="#bbbbbb",
              font=("Ubuntu Mono", 13, "bold")).pack(pady=8, padx=13,)

        ttk.Separator(self.main_frame, orient=HORIZONTAL).pack(fill=X)

        Label(self.main_frame, text=f"Version: 2", bg="#bbbbbb",
              font=("Ubuntu Mono", 13, "bold")).pack(pady=8, padx=13)
        Label(self.main_frame, text=f"Tk Version: {TkVersion}", bg="#bbbbbb",
              font=("Ubuntu Mono", 13, "bold")).pack(pady=8, padx=13)

        ttk.Separator(self.main_frame, orient=HORIZONTAL).pack(fill=X)

        Label(self.main_frame, text=f"OS: {uname().system}", bg="#bbbbbb",
              font=("Ubuntu Mono", 13, "bold")).pack(pady=8, padx=13)

        Label(self.main_frame, text=f"Copyright © Musa Wong 2019-2021", bg="#bbbbbb",
              font=("Ubuntu Mono", 13, "bold")).pack(pady=8, padx=13)

        # # # # # # Buttons # # # # # # #
        closebtn = ttk.Button(self, text="Close", command=lambda: self.destroy())
        # closebtn.configure(highlightbackground="black")
        closebtn.pack(pady=5, side=BOTTOM)

        # Call the mainloop
        self.mainloop()


if __name__ == '__main__':
    HelpWindow()
    # print(uname().system + ",", uname().node, uname().processor, "bit")
