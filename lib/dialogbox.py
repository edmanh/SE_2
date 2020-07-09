import tkinter as tk


class DialogBox(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__()
        print('Opening Toplevel')
        top = self
        top.details_expanded = False
        top.title(title)
        top.geometry(f"300x120+{self.master.winfo_x()}+{self.master.winfo_y()}")
        top.resizable(False, False)
        top.rowconfigure(0, weight=0)
        top.rowconfigure(1, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.info = tk.Text(self, wrap=tk.WORD, height=3, width=20, padx=5, pady=5)
        top.info.insert(tk.END, message)
        top.info.grid(row=0, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky="ew")
        top.quit = tk.Button(self, text="AFBREKEN", command=self.destroy)
        top.quit.grid(row=1, column=1, pady=(7, 7), padx=(10, 10), sticky="e")
        top.ok = tk.Button(self, text="DOORGAAN", command=self.destroy)
        top.ok.grid(row=1, column=1, pady=(7, 7), padx=(10, 10), sticky="w")


    def close(self):
        self.destroy()

    def close_me(self):
        self.destroy()

