# import tkinter as tk
# import tkinter.ttk as ttk
#
#
# class FindWindow(tk.Toplevel):
#     def __init__(self, master, **kwargs):
#         super().__init__(**kwargs)
#
#         self.master = master
#
#         self.geometry('450x140')
#         self.resizable(0, 0)
#         self.title('Find and Replace')
#         self.transient(self.master)
#
#         self.text_to_find = tk.StringVar()
#         self.text_to_replace_with = tk.StringVar()
#
#         top_frame = tk.Frame(self)
#         middle_frame = tk.Frame(self)
#         bottom_frame = tk.Frame(self)
#
#         find_entry_label = ttk.Label(top_frame, text="Find: ", style="editor.TLabel")
#         self.find_entry = ttk.Entry(top_frame, textvar=self.text_to_find)
#
#         replace_entry_label = ttk.Label(middle_frame, text="Replace: ", style="editor.TLabel")
#         self.replace_entry = ttk.Entry(middle_frame, textvar=self.text_to_replace_with)
#
#         self.find_button = ttk.Button(bottom_frame, text="Find", command=self.on_find, style="editor.TButton")
#         self.replace_button = ttk.Button(bottom_frame, text="Replace", command=self.on_replace, style="editor.TButton")
#         self.cancel_button = ttk.Button(bottom_frame, text="Cancel", command=self.on_cancel, style="editor.TButton")
#
#         find_entry_label.pack(side=tk.LEFT, padx=(20, 0))
#         self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
#
#         replace_entry_label.pack(side=tk.LEFT)
#         self.replace_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
#
#         self.find_button.pack(side=tk.LEFT, padx=(85, 0))
#         self.replace_button.pack(side=tk.LEFT, padx=(20, 20))
#         self.cancel_button.pack(side=tk.RIGHT, padx=(0, 30))
#
#         top_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=30)
#         middle_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=30)
#         bottom_frame.pack(side=tk.TOP, expand=1, fill=tk.X)
#
#         self.find_entry.focus_force()
#
#         self.protocol("WM_DELETE_WINDOW", self.on_cancel)
#
#     def on_find(self):
#         self.master.find(self.text_to_find.get())
#
#     def on_replace(self):
#         self.master.replace_text(self.text_to_find.get(), self.text_to_replace_with.get())
#
#     def on_cancel(self):
#         self.master.cancel_find()
#         self.destroy()
#
#
# if __name__ == '__main__':
#     mw = tk.Tk()
#     fw = FindWindow(mw)
#     mw.mainloop()



import re
import sys
import tkinter
from tkinter import ttk
from typing import Any, Iterator, List, Tuple, cast

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

class Finder(tkinter.Frame):
    """A widget for finding and replacing text.

    Use the pack geometry manager with this widget.
    """

    def __init__(self, parent: tkinter.Tk, textwidget: tkinter.Text, bg, **kwargs: Any) -> None:
        super().__init__(parent, **kwargs)      # type: ignore
        self.bg=bg
        self.config(bg=bg)
        self._textwidget = textwidget

        # grid layout:
        #         column 0        column 1     column 2        column 3
        #     ,---------------------------------------------------------------.
        # row0|     Find:     | text entry    |       | [x] Full words only   |
        #     |---------------|---------------|-------|-----------------------|
        # row1| Replace with: | text entry    |       | [x] Ignore case       |
        #     |---------------------------------------------------------------|
        # row2| button frame, this thing contains a bunch of buttons          |
        #     |---------------------------------------------------------------|
        # row3| status label with useful-ish text                             |
        #     |---------------------------------------------------------------|
        # row4| separator                                                     |
        #     `---------------------------------------------------------------'
        #
        # note that column 2 is used just for spacing, the separator helps
        # distinguish this from e.g. status bar below this
        self.grid_columnconfigure(2, minsize=30)
        self.grid_columnconfigure(3, weight=1)

        # TODO: use the pygments theme somehow?
        textwidget.tag_config(
            'find_highlight', foreground='black', background='yellow')
        self._textwidget.tag_lower('find_highlight', 'sel')

        self.find_entry = self._add_entry(0, "Find:")
        find_var = tkinter.StringVar()
        self.find_entry.config(textvariable=find_var)
        find_var.trace_add('write', self.highlight_all_matches)

        # because cpython gc
        cast(Any, self.find_entry).lol = find_var

        self.replace_entry = self._add_entry(1, "Replace with:")

        self.find_entry.bind('<Shift-Return>', self._go_to_previous_match, add=True)
        self.find_entry.bind('<Return>', self._go_to_next_match, add=True)

        # commented out because pressing tab in self.find_entry unselects the
        # text in textwidget for some reason
        #self.replace_entry.bind('<Return>', self._replace_this)

        buttonframe = tkinter.Frame(self)
        buttonframe["bg"] = bg
        buttonframe.grid(row=2, column=0, columnspan=4, sticky='we')

        self.previous_button = ttk.Button(buttonframe, text="Previous match",
                                          command=self._go_to_previous_match)
        self.next_button = ttk.Button(buttonframe, text="Next match",
                                      command=self._go_to_next_match)
        self.replace_this_button = ttk.Button(
            buttonframe, text="Replace this match",
            command=self._replace_this)
        self.replace_all_button = ttk.Button(
            buttonframe, text="Replace all",
            command=self._replace_all)

        self.previous_button.pack(side='left')
        self.next_button.pack(side='left')
        self.replace_this_button.pack(side='left')
        self.replace_all_button.pack(side='left')
        self._update_buttons()

        self.full_words_var = tkinter.BooleanVar()
        self.full_words_var.trace_add('write', self.highlight_all_matches)
        self.ignore_case_var = tkinter.BooleanVar()
        self.ignore_case_var.trace_add('write', self.highlight_all_matches)

        # TODO: add keyboard shortcut for "Full words only". I use it all the
        #       time and reaching mouse is annoying. Tabbing through everything
        #       is also annoying.
        ttk.Checkbutton(
            self, text="Full words only", variable=self.full_words_var).grid(
                row=0, column=3, sticky='w')
        ttk.Checkbutton(
            self, text="Ignore case", variable=self.ignore_case_var).grid(
                row=1, column=3, sticky='w')

        self.statuslabel = ttk.Label(self)
        self.statuslabel.grid(row=3, column=0, columnspan=4, sticky='we')

        ttk.Separator(self, orient='horizontal').grid(
            row=4, column=0, columnspan=4, sticky='we')

        # closebutton = ttk.Button(self, cursor='hand2', text="X")
        closebutton = tkinter.Button(self, text='X', command=lambda: self.hide(),
                          background="#3C3F41", foreground="white", activebackground="red", width="10", height=5, bd=0)
        closebutton.place(relx=1, rely=0, anchor='ne')
        def hover(event=None):
            closebutton["background"] = "#C10D1C"
        def nothover(event=None):
            closebutton["background"] = "#3C3F41"
        closebutton.bind("<Enter>", hover)
        closebutton.bind("<Leave>", nothover)

        self.style = ttk.Style(self)
        self.style.configure("TLabel", background=bg, foreground="white")
        self.style.configure("TButton", background=bg)
        self.style.configure("TCheckbutton", background=bg, foreground="white")
        self.style.configure("TEntry", background="black", foreground="black")


    def _add_entry(self, row: int, text: str) -> ttk.Entry:
        ttk.Label(self, text=text).grid(row=row, column=0, sticky='w')
        entry = ttk.Entry(self, width=35, font='TkFixedFont')
        entry.bind('<Escape>', self.hide, add=True)
        entry.grid(row=row, column=1, sticky='we')
        return entry

    def show(self) -> None:
        self.pack(fill='x')
        self.find_entry.focus_set()
        self.highlight_all_matches()

    def hide(self, junk: object = None) -> None:
        # remove previous highlights from highlight_all_matches
        self._textwidget.tag_remove('find_highlight', '1.0', 'end')

        self.pack_forget()
        self._textwidget.focus_set()

    # tag_ranges returns (start1, end1, start2, end2, ...), and this thing
    # gives a list of (start, end) pairs
    def get_match_ranges(self) -> List[Tuple[str, str]]:
        starts_and_ends = list(
            map(str, self._textwidget.tag_ranges('find_highlight')))
        assert len(starts_and_ends) % 2 == 0
        pairs = list(zip(starts_and_ends[0::2], starts_and_ends[1::2]))
        return pairs

    # must be called when going to another match or replacing becomes possible
    # or impossible, i.e. when find_highlight areas or the selection changes
    def _update_buttons(self, junk: object = None) -> None:
        State = Literal['normal', 'disabled']
        matches_something_state: State = 'normal' if self.get_match_ranges() else 'disabled'
        replace_this_state: State

        try:
            start, end = map(str, self._textwidget.tag_ranges('sel'))
        except ValueError:
            replace_this_state = 'disabled'
        else:   # no, elif doesn't work here
            if (start, end) in self.get_match_ranges():
                replace_this_state = 'normal'
            else:
                replace_this_state = 'disabled'

        self.previous_button.config(state=matches_something_state)
        self.next_button.config(state=matches_something_state)
        self.replace_this_button.config(state=replace_this_state)
        self.replace_all_button.config(state=matches_something_state)

    def _get_matches_to_highlight(self, looking4: str) -> Iterator[str]:
        nocase_opt = self.ignore_case_var.get()
        if self.full_words_var.get():
            # tk doesn't have python-style \b, but it has \m and \M that match
            # the beginning and end of word, see re_syntax(3tcl)
            #
            # TODO: are there \w characters that need to be escaped? this is
            # validated in highlight_all_matches()
            search_arg = r'\m' + looking4 + r'\M'
            regexp_opt = True
        else:
            search_arg = looking4
            regexp_opt = False

        start_index = '1.0'
        first_time = True

        while True:
            # searching at the beginning of a match gives that match, not
            # the next match, so we need + 1 char... unless we are looking
            # at the beginning of the file, and to avoid infinite
            # recursion, we check for that by checking if we have done it
            # before
            if first_time:
                start_index_for_search = start_index
                first_time = False
            else:
                start_index_for_search = '%s + 1 char' % start_index

            start_index = self._textwidget.search(
                search_arg, start_index_for_search, 'end',
                nocase=nocase_opt, regexp=regexp_opt)
            if not start_index:
                # no more matches
                break
            yield start_index

    def highlight_all_matches(self, *junk: object) -> None:
        # clear previous highlights
        self._textwidget.tag_remove('find_highlight', '1.0', 'end')

        looking4 = self.find_entry.get()
        if not looking4:    # don't search for empty string
            self._update_buttons()
            self.statuslabel.config(text="Type something to find.")
            return
        if self.full_words_var.get():
            # check for non-wordy characters
            match = re.search(r'\W', looking4)
            if match is not None:
                self._update_buttons()
                self.statuslabel.config(
                    text=f'The search string can\'t contain "{match.group(0)}" when "Full words only" is checked.'
                )
                return

        count = 0
        for start_index in self._get_matches_to_highlight(looking4):
            self._textwidget.tag_add(
                'find_highlight', start_index,
                '%s + %d chars' % (start_index, len(looking4)))
            count += 1

        self._update_buttons()
        if count == 0:
            self.statuslabel.config(text="Found no matches :(")
        elif count == 1:
            self.statuslabel.config(text="Found 1 match.")
        else:
            self.statuslabel.config(text=f"Found {count} matches.")

    def _select_range(self, start: str, end: str) -> None:
        self._textwidget.tag_remove('sel', '1.0', 'end')
        self._textwidget.tag_add('sel', start, end)
        self._textwidget.mark_set('insert', start)
        self._textwidget.see(start)

    def _go_to_next_match(self, junk: object = None) -> None:
        pairs = self.get_match_ranges()
        if not pairs:
            # the "Next match" button is disabled in this case, but the key
            # binding of the find entry is not
            self.statuslabel.config(text="No matches found!")
            return

        # find first pair that starts after the cursor
        for start, end in pairs:
            if self._textwidget.compare(start, '>', 'insert'):
                self._select_range(start, end)
                break
        else:
            # reached end of file, use the first match
            self._select_range(*pairs[0])

        self.statuslabel.config(text="")
        self._update_buttons()

    # see _go_to_next_match for comments
    def _go_to_previous_match(self, junk: object = None) -> None:
        pairs = self.get_match_ranges()
        if not pairs:
            self.statuslabel.config(text="No matches found!")
            return

        for start, end in reversed(pairs):
            if self._textwidget.compare(start, '<', 'insert'):
                self._select_range(start, end)
                break
        else:
            self._select_range(*pairs[-1])

        self.statuslabel.config(text="")
        self._update_buttons()
        return

    def _replace_this(self, junk: object = None) -> None:
        if str(self.replace_this_button.cget('state')) == 'disabled':
            self.statuslabel.config(text='Click "Previous match" or "Next match" first.')
            return

        # highlighted areas must not be moved after .replace, think about what
        # happens when you replace 'asd' with 'asd'
        start, end = self._textwidget.tag_ranges('sel')
        self._textwidget.tag_remove('find_highlight', start, end)
        self._update_buttons()
        self._textwidget.replace(start, end, self.replace_entry.get())

        self._textwidget.mark_set('insert', start)
        self._go_to_next_match()

        left = len(self.get_match_ranges())
        if left == 0:
            self.statuslabel.config(text="Replaced the last match.")
        elif left == 1:
            self.statuslabel.config(text="Replaced a match. There is 1 more match.")
        else:
            self.statuslabel.config(text=f"Replaced a match. There are {left} more matches.")

    def _replace_all(self) -> None:
        match_ranges = self.get_match_ranges()

        # must do this backwards because replacing may screw up indexes AFTER
        # the replaced place
        for start, end in reversed(match_ranges):
            self._textwidget.replace(start, end, self.replace_entry.get())
        self._textwidget.tag_remove('find_highlight', '1.0', 'end')
        self._update_buttons()

        if len(match_ranges) == 1:
            self.statuslabel.config(text="Replaced 1 match.")
        else:
            self.statuslabel.config(text=f"Replaced {len(match_ranges)} matches.")


if __name__ == '__main__':
    w = tkinter.Tk()
    t = tkinter.Text()
    t.pack(fill="both", expand=True)
    f = Finder(w, t, bg="#262626", height=3)
    f.pack(fill="x")
    w.mainloop()
