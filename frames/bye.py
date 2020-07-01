import tkinter as tk
from tkinter import ttk

import lib.config as cnf
import lib.globals as gl
from lib.functions import lineno
from lib.functions import set_dpi_awareness

set_dpi_awareness()

class ByeBye(ttk.Frame):
    def __init__(self, parent, controller):
        """ parent = container frame,
            controller = sereporter class """
        super().__init__(parent)

        self.controller = controller
        self.config(style='Panel.TFrame')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        print(f'{__name__}, {lineno()}: page_name = bye')

        page_label = ttk.Label(self, text=' TER INFORMATIE ', padding=10,
                     style='PanelLabel.TLabel')
        page_label.grid(row=0, column=0, padx=20, pady=20)

        self.text_field = tk.Text(self, height=4, width=40, font=cnf.fh14, bd=4, padx=10, pady=10)
        self.text_field.grid(row=1, column=0, padx=20, pady=20, ipadx=10, ipady=10)
        self.text_field.insert(tk.END, controller.message.get())

        quit_button = ttk.Button(self, text='Sluiten', style='MenuButton.TButton',
                                 command=lambda: self.accept())
        quit_button.grid(row=2, column=0, pady=100) # , sticky='EW'

    def set_text(self, text):
        print(f'{__name__}-{lineno()} message (bye) = {text}')
        self.text_field.delete(1.0, tk.END)
        self.text_field.insert(tk.END, text)

        #  self.after(gl.wait_for_quit, self.accept)

    def accept(self):
        self.controller.close_app()

