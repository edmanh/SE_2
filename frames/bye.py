import tkinter as tk
from tkinter import ttk
import lib.config as cnf
import lib.globals as gl
from lib.functions import lineno
from lib.functions import set_dpi_awareness

set_dpi_awareness()


class ByeBye(ttk.Frame):
    geo = '500x500+100+100'

    def __init__(self, parent, controller):
        """ parent = container frame,
            controller = sereporter class """
        super().__init__(parent)

        self.controller = controller
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config(style='Panel.TFrame')
        self.configure(width=40, height=80)
        self.grid(row=0, column=0, sticky='nesw')

        inside = ttk.Frame(self, style='Panel.TFrame')
        inside.grid(padx=30, pady=30)

        page_label = ttk.Label(inside, text=' TER INFORMATIE ', padding=10,
                     style='PanelLabel.TLabel')
        page_label.grid(row=0, column=0, padx=20, pady=20)

        self.text_field = tk.Text(inside, height=5, width=32, font=cnf.fh12, bd=4, padx=10, pady=10)
        self.text_field.grid(row=1, column=0, padx=20, pady=20, ipadx=10, ipady=10)
        self.text_field.insert(tk.END, controller.message.get())

        quit_button = ttk.Button(inside, text='Sluiten', style='MenuButton.TButton',
                                 command=lambda: self.accept())
        quit_button.grid(row=2, column=0, pady=10)

    def set_text(self, text):
        self.text_field.delete(1.0, tk.END)
        self.text_field.insert(tk.END, text)

    def accept(self):
        self.controller.close_app()

