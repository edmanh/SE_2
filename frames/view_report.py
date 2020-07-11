import os
from os import path
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as stxt
from tkinter import filedialog as fd
from lib.functions import lineno
from lib.functions import set_dpi_awareness
import lib.config as cnf
import lib.globals as gl
from lib.formatter import FormatIt

set_dpi_awareness()

class ViewReport(ttk.Frame):
    geo = '800x900'

    def __init__(self, parent, controller):
        """ parent = Frame container,
            controller = class SeReporter() """
        super().__init__(parent)

        self.parent = parent
        self.controller = controller
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(style='Panel.TFrame')

        inside = ttk.Frame(self, style='Panel.TFrame')  # width=300,
        inside.grid(padx=20, pady=20)
        l1 = ttk.Label(inside, text=' Bewaard rapport inzien ', style='PanelLabel.TLabel')
        l1.grid(row=0, column=0, sticky='WE')

        if self.controller.tmp_file:
            button0 = ttk.Button(inside, text='Opslaan als ...',
                                 style='MenuButton.TButton',
                                 width=20,
                                 command=self.fini)
            button0.grid(row=1, column=0, pady=10, sticky='E')
        else:
            button1 = ttk.Button(inside, text='Selecteer een rapport',
                                 style='MenuButton.TButton',
                                 width=20,
                                 command=self.getfile)
            button1.grid(row=1, column=0, pady=10, sticky='W')

        self.txt = stxt.ScrolledText(inside, height=40, width=80, bg='#fffaf1', padx=10, pady=10)
        self.txt.grid(row=2, column=0, padx=10, pady=10)
        self.txt.delete('1.0', tk.END)
        self.txt.insert(tk.END, 'Nog geen file gekozen')


        button2 = ttk.Button(inside, text='Klaar',
                             style='MenuButton.TButton',
                             width=20,
                             command=self.fini)
        button2.grid(row=3, column=0, pady=10, sticky='E')


    def getfile(self):
        try:
            name = fd.askopenfilename()
        except:
            self.txt.delete('1.0', tk.END)
            self.txt.insert(tk.END, 'Bestandskeuze is niet geldig')
            return
        try:
            content = open(name, 'r').read(10000000)
        except IOError:
            content = ''
            self.txt.delete('1.0', tk.END)
            self.txt.insert(tk.END, 'Bestand is niet leesbaar')

        self.myjson = FormatIt(4)  # Parameter is tab size in number of spaces
        self.myjson.reset()

        output = '\n'
        report_dir = os.path.basename(os.path.dirname(name))
        report = '..../' + report_dir + '/' + path.split(name)[1]
        header = f'Gekozen rapport: {report}'
        subheader = '=' * len(header)
        output += header + '\n'
        output += subheader + '\n'

        self.myjson.reset()
        self.myjson.format_me(content)
        for txt in self.myjson.output:
            output += txt + '\n'

        self.txt.delete('1.0', tk.END)
        self.txt.insert(tk.END, output)



    def cont(self):
        pass

    def fini(self):
        self.controller.lastframe()
        pass

    def set_text(self, txt):
        pass

