import tkinter as tk
from tkinter import ttk
from tkinter import font  as tkfont
from lib.functions import lineno
from lib.functions import set_dpi_awareness
import lib.config

set_dpi_awareness()

class Desk(ttk.Frame):
    geo = '500x600+100+100'

    def __init__(self, parent, controller):
        """ parent = Frame container,
            controller = class SeReporter() """
        super().__init__(parent)

        self.controller = controller
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(style='Panel.TFrame')
        self.configure(width=40, height=80)
        self.grid(row=0, column=0, sticky='nesw')
        self.report_type = ''

        inside = ttk.Frame(self, style='Panel.TFrame')
        inside.grid(padx=30, pady=30)

        label = ttk.Label(inside, text="Welkom bij SE reporter", style='PanelLabel.TLabel')
        label.grid(row=0, column=0, pady=10, padx=20, sticky='EW')

        button1 = ttk.Button(inside, text='Bestaande rapporten inzien',
                             style='MenuButton.TButton',
                             width=30,
                             command=lambda: controller.show_frame('ViewReport'))
        button1.grid(row=1, column=0, pady=10)

        button2 = ttk.Button(inside, text="Nieuw rapport ophalen",
                             style='MenuButton.TButton',
                             width=30,
                             command=lambda: controller.show_frame('ReportTypeMenu'))
        button2.grid(row=2, column=0, pady=10)

        button3 = ttk.Button(inside, text="Afbreken",
                             style='MenuButton.TButton',
                             width=30,
                             command=lambda: self.close_me())
        button3.grid(row=3, column=0, pady=10)

    def close_me(self):
        msg = 'Een beetje snel maar OK,\nVolgende keer beter.'
        self.controller.set_message(msg)
        print(f'{__name__}-{lineno()} Val = {self.controller.message}')
        self.controller.show_frame("ByeBye")

    def set_text(self, txt):
        pass
