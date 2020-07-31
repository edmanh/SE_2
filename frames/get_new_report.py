import os
from os import path
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as stxt
from tkinter import filedialog as fd
import requests
from lib.functions import lineno
from lib.functions import set_dpi_awareness
import lib.config as cnf
import lib.globals as gl
from lib.formatter import FormatIt
from lib.dialogbox import DialogBox

api = gl.MyApi
NwReport = gl.MyReport
cwd = os.getcwd()
set_dpi_awareness()


class GetNewReport(ttk.Frame):
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
        self.url_site = ''

        self.tdir = tk.StringVar()
        self.tdir.set('')
        self.tfile = tk.StringVar()
        self.tfile.set('')

        inside = ttk.Frame(self, style='Panel.TFrame')  # width=300,
        inside.grid(padx=20, pady=20)
        self.l1 = ttk.Label(inside, text=' Nieuw rapport opvragen ', style='PanelLabel.TLabel')
        self.l1.grid(row=0, column=0, sticky='WE')

        buttons = ttk.Frame(inside, style='Panel.TFrame')  # width=300,
        buttons.grid(row=6, padx=0, pady=[20, 10])

        button2 = ttk.Button(buttons, text='Terug',
                             style='MenuButton.TButton',
                             width=20,
                             command=self.go_back)
        button2.grid(row=0, column=2, padx=10, pady=0)  # , sticky='W'

        button3 = ttk.Button(buttons, text='Opslaan',
                             style='MenuButton.TButton',
                             width=20,
                             command=self.save)
        button3.grid(row=0, column=3, padx=10, pady=0)  # , sticky='W'

        self.txt = stxt.ScrolledText(inside, height=24, width=80, bg='#fffaf1', padx=10, pady=10)
        self.txt.grid(row=2, column=0, padx=10, pady=10)
        self.txt.delete('1.0', tk.END)
        self.txt.insert(tk.END, 'Nog geen rapport opgevraagd')

        # Row 0: Frame 'location dialog'
        frl = tk.LabelFrame(inside, text=' Opslaglokatie ', bg='#ffefd8')
        frl.grid(row=3, column=0, padx=10, pady=5, columnspan=1, sticky='W')
        self.mn = tk.Entry(frl, textvariable=self.tdir, width=45, font=cnf.fh12)
        self.mn.grid(row=0, column=0, padx=(5, 20), pady=10)
        self.mn.bind('<Return>', self.set_dir)

        # Row 1: Frame 'file name dialog'
        frf = tk.LabelFrame(inside, text=' Bestandsnaam ', bg='#ffefd8')
        frf.grid(row=4, column=0, padx=10, pady=5, sticky='W')
        self.fn = tk.Entry(frf, textvariable=self.tfile, width=30, font=cnf.fh12)  # height=1,
        self.fn.grid(row=0, column=0, padx=(5, 20), pady=10)
        self.fn.bind('<Return>', self.set_file_name)

        # Row 2: Resulting 'save as'    # , height=1, anchor='w', padx=5, bd=3, relief=tk.SUNKEN
        frs = tk.LabelFrame(inside, text=' Opslaan als ... ', bg='#ffefd8')
        frs.grid(row=5, column=0, padx=10, pady=5, sticky='W')
        self.te = tk.Label(frs, text='', width=70, font=cnf.fh11, bg='#ffefd8')
        self.te.grid(row=0, column=0, padx=(5, 20), pady=10)

        # ================================ END OF INIT =====================================

    def go(self):
        self.url_site = f'https://monitoringapi.solaredge.com/site/{cnf.my_id}/{api.name}'
        print(f'{__name__}-{lineno()}: Called from set_new_report')
        self.l1['text'] = f' Actueel rapport --{cnf.all_titles.get(api.name)}-- '
        # Prepare saving the report
        this_date = datetime.date.today().strftime('%Y-%m-%d')
        if cnf.report_dir[0] in ('/', '\\'):
            NwReport.file_dir = cnf.report_dir
        else:
            NwReport.file_dir = cwd + '\\' + cnf.report_dir
        self.tdir.set(NwReport.file_dir)
        NwReport.file_name = api.name + '@' + this_date + '.txt'
        self.tfile.set(NwReport.file_name)
        self.te['text'] = f'{self.tdir.get()}{self.tfile.get()}'
        self.api_get_report()
        return

    def api_get_report(self):
        header = ''
        NwReport.file_content = ''
        if cnf.project_alive:
            api.url_args['api_key'] = cnf.my_key
            response = requests.get(self.url_site, api.url_args)
            print(f'requests.get acts on: {response.url}')
            if not response.status_code == requests.codes.ok:
                msg = f'\tEr ging iets mis met deze opdracht, sorry!\n De server gaf errorcode {response.status_code}'
                msg = msg + f'De url was: {response.url}'
                msg = msg + f'Ontvangen tekst: {response.text}'
                self.txt.delete('1.0', tk.END)
                self.txt.insert(tk.END, msg)
            else:
                header = f'Rapport betreffende: {api.name}'
                NwReport.file_content = response.text
        else:
            with open(cnf.report_dir + '\\timeFrameEnergy.txt', 'r') as myfile:
                NwReport.file_content = myfile.read().replace('\n', '')
            header = 'Rapport op basis van testfile'

        myjson = FormatIt(4)  # Parameter is tab size in number of spaces
        myjson.reset()
        output = '\n'
        subheader = '=' * len(header)
        output += header + '\n'
        output += subheader + '\n'
        myjson.format_me(NwReport.file_content)
        for line in myjson.output:
            output += line + '\n'
        gl.doccontent = output

        # Show received report
        self.txt.delete('1.0', tk.END)
        self.txt.insert(tk.END, output)

    def save(self):
        top = tk.Toplevel(None)
        top.title = 'Saving - Changing'
        try:
            fptr = fd.asksaveasfile(mode='w',
                                    initialfile=self.tfile.get(),
                                    initialdir=self.tdir.get()
                                    )
            if fptr:
                fptr.write(NwReport.file_content)
                fptr.close()
                gl.user_choice = 'saved'
        except IOError:
            msg = f'Probleem bij opslaan'
            self.txt.delete('1.0', tk.END)
            self.txt.insert(tk.END, msg)
        top.destroy()
        return

    def cont(self):
        pass

    def go_back(self):
        self.controller.lastframe()
        pass

    def set_text(self, txt):
        pass

    def call_dialog(self, *args, **kwargs):
        d = DialogBox(self, *args, **kwargs)
        d.grab_set()
        self.wait_window(d)
        d.grab_release()
        #  print(f'BACK after wait with gl.next_step = {gl.next_step}')
        return

    def set_dir(self, x):
        # self.controller.attributes("-topmost", True)
        if not cnf.project_alive:
            print(f'x = {x}')
        new_dir = self.mn.get()
        if new_dir[-1] not in ('\\', '/'):
            new_dir += '\\'
        self.tdir.set(new_dir)
        self.te['text'] = f'{self.tdir.get()}{self.tfile.get()}'

    def set_file_name(self, x):
        # self.controller.attributes("-topmost", True)
        if not cnf.project_alive:
            print(f'x = {x}')
        new_file = self.fn.get()
        self.tfile.set(new_file)
        self.te['text'] = f'{self.tdir.get()}{self.tfile.get()}'


'''
        button1 = ttk.Button(buttons, text='Start ophalen',
                             style='MenuButton.TButton',
                             width=20,
                             command=self.api_get_report)
        button1.grid(row=0, column=1, padx=10, pady=0)  # , sticky='W'

        dp = dict()
        dp.clear()
        dp['title'] = 'Vraagje ..'
        dp['message'] = 'Rapport opslaan als {NwReport["file"]} in {NwReport["dir"]}?'
        dp['deny'] = 'Terug'
        dp['accept'] = 'Opslaan graag'
        self.call_dialog(**dp)

        if gl.next_step == 'no action':
            return


        # Saving report
        pd['text'] = 'Onbekende fout ervaren'
        if gl.user_choice == 'cancel':
            pd['text'] = 'Jammer,\nvolgende keer beter.'
        if gl.user_choice == 'saved':
            pd['text'] = 'Gelukt!\nRapport is opgeslagen.'
        if gl.user_choice == 'problem':
            pd['text'] = 'Er is iets onduidelijks misgegaan,\nprobeer het later nog eens.'
        pd['func'] = 'info'
        pd['auto_close'] = 5000
        panels.dialogs(**pd)

        #  bye(lineno())
        
'''