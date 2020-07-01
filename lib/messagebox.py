import tkinter as tk


class TopMessage(tk.Toplevel):
    def close_me(self):
        self.destroy()

    def __init__(self, delay, title, message):
        super().__init__()
        self.details_expanded = False
        self.title(title)
        self.geometry(f"300x120+{self.master.winfo_x()}+{self.master.winfo_y()}")
        self.resizable(False, False)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.info = tk.Text(self, wrap=tk.WORD, height=3, width=20, padx=5, pady=5)
        self.info.insert(tk.END, message)
        self.info.grid(row=0, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky="ew")
        self.ok = tk.Button(self, text="SLUIT", command=self.destroy)
        self.ok.grid(row=1, column=1, pady=(7, 7), padx=(10, 10), sticky="e")
        self.after(delay, self.close_me)

    def close(self):
        self.destroy()
