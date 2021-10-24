import tkinter as tk
import tkinter.messagebox as msg



class MyText(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)

        self.master = master

        self.config(wrap=tk.WORD)  # CHAR NONE

        # self.tag_configure('find_match', background="#595959")
        self.tag_configure('find_match', background="#2B2B2B")
        self.find_match_index = None
        self.find_search_starting_index = 1.0

    def find(self, text_to_find):
        length = tk.IntVar()
        idx = self.search(text_to_find, self.find_search_starting_index, stopindex=tk.END, count=length)

        if idx:
            self.tag_remove('find_match', 1.0, tk.END)

            end = f'{idx}+{length.get()}c'
            self.tag_add('find_match', idx, end)
            self.see(idx)

            self.find_search_starting_index = end
            self.find_match_index = idx
        else:
            if self.find_match_index != 1.0:
                if msg.askyesno("No more results", "No further matches. Repeat from the beginning?"):
                    self.find_search_starting_index = 1.0
                    self.find_match_index = None
                    return self.find(text_to_find)
            else:
                msg.showinfo("No Matches", "No matching text found")

    def replace_text(self, target, replacement):
        if self.find_match_index:
            current_found_index_line = str(self.find_match_index).split('.')[0]

            end = f"{self.find_match_index}+{len(target)}c"
            self.replace(self.find_match_index, end, replacement)

            self.find_search_starting_index = current_found_index_line + '.0'

    def cancel_find(self):
        self.find_search_starting_index = 1.0
        self.find_match_index = None
        self.tag_remove('find_match', 1.0, tk.END)

    def display_file_contents(self, filepath):
        with open(filepath, 'r') as file:
            self.delete(1.0, tk.END)
            self.insert(1.0, file.read())