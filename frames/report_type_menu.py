import tkinter as tk
from tkinter import ttk
from lib.functions import lineno
import lib.config as cnf
import lib.globals as gl
from lib.functions import set_dpi_awareness

api = gl.MyApi
set_dpi_awareness()

print(f"Var's in {__name__}: {dir()}")

class ReportTypeMenu(ttk.Frame):
    geo = '500x700'

    def __init__(self, parent, controller):
        """ parent = Frame container,
            controller = class SeReporter() """
        super().__init__(parent)

        self.controller = controller
        self.parent = parent
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(style='Panel.TFrame')
        self.configure(width=40, height=80)
        self.grid(row=0, column=0, sticky='nesw')
        controller.set_title(__name__)

        inside = ttk.Frame(self, style='Panel.TFrame')  # width=300,
        inside.grid(padx=30, pady=30)

        label = ttk.Label(inside, text="Keuzemenu Rapporttypen", style='PanelLabel.TLabel')
        label.grid(row=0, column=0, pady=10, padx=20, sticky='EW')

        self.v = tk.StringVar()
        print(f'Start building Radiobutton')
        rownr = 1
        for name, title in cnf.all_titles.items():
            btn = tk.Radiobutton(
                inside,
                text=title,
                indicatoron=0,  # gives buttons not radio choices
                width=20, height=2,
                padx=20,
                variable=self.v,
                cursor='plus',
                background='black', foreground='white',
                font='Helvetica 11',
                command=self.accept,
                value=name)
            btn.grid(row=rownr, column=0, padx=4, pady=2)
            rownr += 1
#            CreateToolTip(btn, 'Ter info:\nDe api naam = ' + api)

        bq = ttk.Button(inside, width=15,
                       text='Terug', style='MenuButton.TButton',
                       command=self.go_back)
        bq.grid(row=rownr, padx=10, pady=20, sticky=tk.E)

    def go_back(self):
        gl.user_choice = ''
        print(f'Called go_back from {self.controller.framehist[-1]}')
        self.controller.lastframe()

    def accept(self):
        api.name = self.v.get()
        self.controller.set_trigger('newReport')
        self.controller.show_frame('SetNewReport')
        self.v.set(None)

    def close_me(self):
        msg = 'Een beetje snel maar OK,\nVolgende keer beter.'
        self.controller.set_message(msg)
        print(f'{__name__}-{lineno()} Val = {self.controller.message}')
        self.controller.show_frame("ByeBye")

    def set_text(self, txt):
        pass
