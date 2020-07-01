import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import lib.globals as gl
from tkinter import font  as tkfont
from lib.functions import lineno
import lib.config


class GetHistReport(ttk.Frame):

    def __init__(self, parent, controller):
        """ parent = Frame container,
            controller = class SeReporter() """
        super().__init__(parent)

        controller.set_title(__name__)
        self.controller = controller
        self.parent = parent
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(style='Panel.TFrame')

        inside = ttk.Frame(self, style='Panel.TFrame')  # width=300,
        inside.grid(padx=30, pady=30)

        label = ttk.Label(inside, text="Rapportkeuze", style='PanelLabel.TLabel')
        label.grid(row=0, column=0, pady=10, padx=20, sticky='EW')

        button1 = ttk.Button(inside, text='START',
                             style='MenuButton.TButton',
                             width=20,
                             command=self.getfile)
        button1.grid(row=1, column=0, pady=10)

        button2 = ttk.Button(inside, text='Afbreken',
                             style='MenuButton.TButton',
                             width=20,
                             command=self.go_back)
        button2.grid(row=2, column=0, pady=10)

    def go_back(self):
        self.controller.lastframe()

    def getfile(self):
        #fr = tk.Frame(self, width=600, height=400)
        #fr.grid()
        name = fd.askopenfilename()
        gl.user_val = 1
        gl.rapfilename = name
        if len(name) < 2:
            gl.user_val = 0
            self.destroy()
        else:
            print(f'Gekozen bestand = {gl.rapfilename}')
            print(f'gl.rapfilename = {gl.rapfilename}')
            print(f'gl.user_val = {gl.user_val}')
            self.controller.set_trigger('show')
            self.controller.show_frame('ViewReport')


    def set_text(self, txt):
        pass
