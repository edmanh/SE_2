import tkinter as tk
from tkinter import Toplevel


class DialogBox(tk.Toplevel):
    def __init__(self, master, title, message):
        super().__init__()
        # top = self.top = Toplevel(master)
        self.details_expanded = False
        self.title(title)
        self.geometry(f"300x120+{master.winfo_x()}+{master.winfo_y()}")
        self.resizable(False, False)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.info = tk.Text(self, wrap=tk.WORD, height=3, width=20, padx=5, pady=5)
        self.info.insert(tk.END, message)
        self.info.grid(row=0, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky="ew")
        self.quit = tk.Button(self, text="AFBREKEN", command=self.destroy)
        self.quit.grid(row=1, column=1, pady=(7, 7), padx=(10, 10), sticky="e")
        self.ok = tk.Button(self, text="DOORGAAN", command=self.destroy)
        self.ok.grid(row=1, column=1, pady=(7, 7), padx=(10, 10), sticky="w")


    def close(self):
        self.destroy()

    def close_me(self):
        self.destroy()

