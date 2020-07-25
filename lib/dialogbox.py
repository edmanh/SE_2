import tkinter as tk
import lib.globals as gl


class DialogBox(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__()
        self.parent = parent
        top = self
        top.details_expanded = False
        top.title(kwargs['title'])
        top.geometry(f"300x120+{self.master.winfo_x()}+{self.master.winfo_y()}")
        top.resizable(False, False)
        top.rowconfigure(0, weight=0)
        top.rowconfigure(1, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.info = tk.Text(self, wrap=tk.WORD, height=3, width=20, padx=5, pady=5)
        top.info.insert(tk.END, kwargs['message'])
        top.info.grid(row=0, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky="ew")
        top.quit = tk.Button(self, text=kwargs['deny'], command=self.close_me)
        top.quit.grid(row=1, column=1, pady=(7, 7), padx=(10, 10), sticky="e")
        top.ok = tk.Button(self, text=kwargs['accept'], command=self.next_step)
        top.ok.grid(row=1, column=1, pady=(7, 7), padx=(10, 10), sticky="w")


    def close_me(self):
        # just close dialog
        gl.next_step = 'no action'
        self.destroy()

    def next_step(self):
        # Continue with proposed action
        gl.next_step = 'go on'
        self.destroy()

