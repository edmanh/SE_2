import os
from datetime import datetime
from dateutil import relativedelta
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from lib.functions import lineno
from lib.functions import selogger
from lib.functions import set_dpi_awareness
import lib.globals as gl
import lib.config as cnf
import lib.functions as func
from lib.api import CallApi
from lib.messagebox import TopMessage

set_dpi_awareness()


class SetNewReport(ttk.Frame):
    geo = '600x800+50+50'

    def __init__(self, parent, controller):
        """ parent = Frame container,
            controller = class SeReporter() """
        super().__init__(parent)

        self.controller = controller
        self.parent = parent
        self.TopMessage = TopMessage
        self.url_fields = []
        self.api_name = ''
        self.titel_var = tk.StringVar()
        self.choice_var = tk.StringVar()
        self.protocol_var = tk.StringVar()
        self.val_strt_hr = tk.StringVar()
        self.val_strt_min = tk.StringVar()
        self.val_end_hr = tk.StringVar()
        self.val_end_min = tk.StringVar()

        # periode start
        self.period_start = ''
        self.p_start = ''
        self.stop_year = 2020
        self.stop_month = 1
        self.stop_day = 1

        # periode end
        self.period_end = ''
        self.p_end = ''
        self.strt_year = 2020
        self.strt_month = 1
        self.strt_day = 1

        self.period_unit = ''

        # accept value
        self.p_mode = ''
        self.p_start = ''
        self.p_stop = ''
        self.p_unit = ''

        self.setval = ''

        # defenitions background Frame
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(style='Panel.TFrame')

        # definitions inside_frame, an internal 2 column frame
        self.inside_frame = ttk.Frame(self, width=600, style='Panel.TFrame')
        self.inside_frame.grid(padx=30, pady=30)

        # row 0 of inside_frame: page_label
        page_label = ttk.Label(self.inside_frame, textvariable=self.titel_var,
                               text=' Rapportperiode samenstellen en rapport opvragen ',
                               style='PanelLabel.TLabel',
                               width=40,  # Width in chars
                               anchor=tk.CENTER)
        page_label.grid(row=0, column=0, pady=(0, 10))

        # row 1 of inside_frame: info_frame,
        info_frame_label = tk.Label(self.inside_frame, text=' Aanwijzingen ', font=cnf.fh12, fg='black', bg='#ffefd8')
        self.info_frame = ttk.LabelFrame(self.inside_frame, text='',
                                         style='Panel.TFrame',
                                         labelwidget=info_frame_label,
                                         relief=tk.GROOVE)
        self.info_choice = ttk.Label(self.info_frame, textvariable=self.choice_var,
                                     text='choice', style='StatusText.TLabel', width=40)
        self.info_choice.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 5))
        self.info_protocol = ttk.Label(self.info_frame, textvariable=self.protocol_var,
                                       text='protocol', style='StatusText.TLabel', width=40)
        self.info_protocol.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 5))

        self.infotext = tk.Text(self.info_frame, bg='#fffae3', wrap=tk.WORD,
                                height=3, width=40,
                                font=cnf.fh12, bd=2, padx=5, pady=5)
        self.infotext.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10)
        self.infotext.insert(tk.END, 'Info text')
        self.info_frame.grid(row=1, column=0, pady=(10, 0), padx=(0, 0))

        # Settings frame contains all settings grouped by row
        settings_frame_label = tk.Label(self.inside_frame, text=' Instellingen ',
                                        font=cnf.fa12, fg='black', bg='#ffefd8')
        self.fr_settings = ttk.LabelFrame(self.inside_frame, text='--',
                                          labelwidget=settings_frame_label,
                                          style='Panel.TFrame',
                                          relief=tk.GROOVE)
        self.fr_settings.grid(row=2, padx=20, pady=10)
        # self.fr_settings.grid_propagate(0)

        # row 1 = Date frames
        # left = start date
        fr_strt_date_label = tk.Label(self.fr_settings, text=' Startdatum ', font=cnf.fa12, fg='black', bg='#ffefd8')
        self.fr_strt_date = ttk.LabelFrame(self.fr_settings, text=' Begin ', width=175, height=80,
                                           labelwidget=fr_strt_date_label,
                                           style='Panel.TFrame',
                                           relief=tk.GROOVE)
        self.fr_strt_date.grid(row=0, column=0, sticky='W', pady=(5, 10), padx=(10, 10))
        self.fr_strt_date.grid_propagate(0)
        self.start_date = DateEntry(self.fr_strt_date, width=12, date_pattern='yyy-mm-dd', font=cnf.fa12,
                                    year=self.strt_year, month=self.strt_month, day=self.strt_day,
                                    background='#0000ff', foreground='white')
        self.start_date.grid(row=0, column=0, padx=20, pady=10)
        #        std_width = self.fr_strt_date.winfo_width()
        # right = stop date
        fr_stop_date_label = tk.Label(self.fr_settings, text=' Stopdatum ', font=cnf.fa12, fg='black', bg='#ffefd8')
        self.fr_stop_date = ttk.LabelFrame(self.fr_settings, text=' ', width=175, height=80,
                                           labelwidget=fr_stop_date_label,
                                           style='Panel.TFrame',
                                           relief=tk.GROOVE)
        self.stop_date = DateEntry(self.fr_stop_date, width=12, date_pattern='yyy-mm-dd', font=cnf.fh12,
                                  year=self.stop_year, month=self.stop_month, day=self.stop_day,
                                  background='blue', foreground='white')
        self.stop_date.grid(row=0, column=1, padx=20, pady=10)

        self.fr_stop_date.grid(row=1, column=1, sticky='E', pady=(5, 10), padx=(10, 10))
        self.fr_stop_date.grid_propagate(0)

        # row 2 = Time frames
        # r2 - left = start time
        fr_strt_time_label = tk.Label(self.fr_settings, text=' Starttijd ', font=cnf.fa12, fg='black', bg='#ffefd8')
        self.fr_strt_time = ttk.LabelFrame(self.fr_settings, text=' Begin ', width=175, height=80,
                                           labelwidget=fr_strt_time_label,
                                           style='Panel.TFrame',
                                           relief=tk.GROOVE)
        self.fr_strt_time.grid(row=1, column=0, sticky='W', pady=(5, 10), padx=(10, 0))
        self.fr_strt_time.grid_propagate(0)

        self.start_time_hr = ttk.Combobox(self.fr_strt_time,
                                            textvariable=self.val_strt_hr,
                                            values=gl.hrlist, font=cnf.fa12, width=2)
        self.start_time_hr.grid(row=0, column=0, padx=(20, 0), pady=(10, 20))
        self.start_time_hr.current(2)
        dd1 = tk.Label(self.fr_strt_time, text=' : ', font=cnf.fh14, fg='black', bg='#ffefd8')
        dd1.grid(row=0, column=1, pady=(10, 20))
        self.start_time_min = ttk.Combobox(self.fr_strt_time,
                                             textvariable=self.val_strt_min,
                                             values=gl.mnlist, font=cnf.fa12, width=2)
        self.start_time_min.grid(row=0, column=2, padx=(0, 20), pady=(10, 20))
        self.start_time_min.current(0)

        # r2 - right = stop time
        fr_stop_time_label = tk.Label(self.fr_settings, text=' Stoptijd ', font=cnf.fa12, fg='black', bg='#ffefd8')
        self.fr_stop_time = ttk.LabelFrame(self.fr_settings, text=' Eind ', width=175, height=80,
                                           labelwidget=fr_stop_time_label,
                                           style='Panel.TFrame',
                                           relief=tk.GROOVE)
        self.stop_time_hr = ttk.Combobox(self.fr_stop_time,
                                          textvariable=self.val_end_hr,
                                          values=gl.hrlist, font=cnf.fa12, width=2)
        self.stop_time_hr.grid(row=0, column=0, padx=(20, 0), pady=(10, 20))
        self.stop_time_hr.current(16)
        dd2 = tk.Label(self.fr_stop_time, text=' : ', font=cnf.fh14, fg='black', bg='#ffefd8')
        dd2.grid(row=0, column=1, pady=(10, 20))
        self.stop_time_min = ttk.Combobox(self.fr_stop_time,
                                           textvariable=self.val_end_min,
                                           values=gl.mnlist, font=cnf.fa12, width=2)
        self.stop_time_min.grid(row=0, column=2, padx=(0, 20), pady=(10, 20))
        self.stop_time_min.current(0)
        self.fr_stop_time.grid(row=1, column=1, sticky='E', pady=(5, 10), padx=(10, 10))
        self.fr_stop_time.grid_propagate(0)

        # r3 - right = Unit frame
        fr_unit_label = tk.Label(self.fr_settings, text=' Interval ', font=cnf.fa12, fg='black', bg='#ffefd8')
        self.fr_unit = ttk.LabelFrame(self.fr_settings, text=' Begin ', width=175, height=100,
                                      labelwidget=fr_unit_label,
                                      style='Panel.TFrame',
                                      relief=tk.GROOVE)
        self.unit_var = tk.StringVar()
        self.unit_var.set(self.setval)
        self.unit = ttk.OptionMenu(self.fr_unit, self.unit_var, *gl.list_of_units_nl, command=self.set_time_unit)
        self.unit_var.set(gl.list_of_units_nl[0])
        self.unit['menu'].configure(font=cnf.fa12)
        self.unit.configure(style='ChoiceButton.TButton')
        self.unit.grid(row=0, column=0, pady=(10, 10), padx=(20, 10))  # , padx=20, pady=10, sticky='E'
        self.fr_unit.grid(row=2, column=1, pady=(10, 10), padx=(10, 10))
        self.fr_unit.grid_propagate(0)

        acceptbutton = tk.Button(self.inside_frame, text='Klaar',
                                 background='black', foreground='white',
                                 width=20, height=2, font=cnf.fa12,
                                 command=lambda: self.accept(self.p_mode))
        acceptbutton.grid(row=6, column=0, sticky='E', padx=0, pady=20)

        backbutton = tk.Button(self.inside_frame, text='Terug',
                                 background='black', foreground='white',
                                 width=20, height=2, font=cnf.fa12,
                                 command=lambda: self.go_back())
        backbutton.grid(row=6, column=0, sticky='W', padx=0, pady=20)

    def set_time_unit(self, val):
        print(f'returned val: {val}')

        pass

    def go(self):
        self.api_name = self.parent.report_type
        # report_tmp_path = os.path.join(cnf.myhome, cnf.tmp_file)
        # print(f'{lineno()} - cnf.tmp_file = {report_tmp_path}')
        # print(f'{lineno()} - self.parent.report_type = {self.api_name}')
        self.titel_var.set(f' Rapportperiode samenstellen en rapport opvragen ')
        self.choice_var.set(f' Raportkeuze = "{cnf.all_titles.get(self.api_name)}"')
        self.protocol_var.set(f' Protocolnaam = "{self.api_name}"')
        # Get values to complete the arg list
        api_args = cnf.all_args[self.api_name][1:]  # args needed for the choosen api, skip translated title
        api_num_args = len(api_args)
        selogger.info(
            f'Gekozen titel: {cnf.all_titles[self.api_name]}, '
            f'de api naam is {self.api_name}, aantal args = {api_num_args}')

        self.infotext.delete('1.0', tk.END)
        self.infotext.insert(tk.END, cnf.api_config[self.api_name]['info'])
        print(cnf.all_args[self.api_name])
        print(f'api_num_args = {api_num_args}')
        print(cnf.api_config[self.api_name]['info'])
        if api_num_args == 0:
            self.fr_unit.grid_remove()
            self.fr_strt_date.grid_remove()
            self.fr_stop_date.grid_remove()
            self.fr_strt_time.grid_remove()
            self.fr_stop_time.grid_remove()
            self.fr_settings.grid_remove()
        else:
            self.fr_settings.grid(row=2, padx=20, pady=10)
            for nwArg in api_args:
                if nwArg in 'startDate':
                    self.fr_strt_date.grid(row=0, column=0, sticky='W', pady=(10, 10), padx=(10, 10))
                    self.fr_stop_date.grid(row=0, column=1, sticky='E', pady=(10, 10), padx=(10, 10))
                if nwArg in 'startTime':
                    self.fr_strt_date.grid(row=0, column=0, sticky='W', pady=(10, 10), padx=(10, 10))
                    self.fr_stop_date.grid(row=0, column=1, sticky='E', pady=(10, 10), padx=(10, 10))
                    self.fr_strt_time.grid(row=1, column=0, sticky='W', pady=(10, 10), padx=(10, 0))
                    self.fr_stop_time.grid(row=1, column=1, sticky='E', pady=(10, 10), padx=(10, 10))
                if nwArg in 'timeUnit':
                    self.fr_unit.grid(row=2, column=1, pady=(10, 10), padx=(10, 10))

            # Fill widgets with last saved values
            arg_db_values = func.get_api_values(self.api_name)  # database action

            if 'timeUnit' in api_args:
                p_unit = arg_db_values['timeUnit']
                self.url_fields.append('timeUnit')
            else:
                p_unit = ''
                self.fr_unit.grid_forget()
            self.p_start = ''
            self.p_mode = ''
            if 'startDate' in api_args:
                self.p_start = arg_db_values['startDate']
                self.p_mode = 'date'
                self.url_fields.append('startDate')
                self.fr_strt_time.grid_forget()
                self.fr_stop_time.grid_forget()
            elif 'startTime' in api_args:
                self.p_start = arg_db_values['startTime']
                self.p_mode = 'time'
                self.url_fields.append('startTime')
            if 'endDate' in api_args:
                self.p_stop = arg_db_values['endDate']
                self.url_fields.append('endDate')
            elif 'endTime' in api_args:
                self.p_stop = arg_db_values['endTime']
                self.url_fields.append('endTime')

            if len(self.p_start) < 4:
                self.p_start = '2020-01-01 12:00:00'
            self.strt_year = int(self.p_start[0:4])
            self.strt_month = int(self.p_start[5:7])
            self.strt_day = int(self.p_start[8:10])
            if len(self.p_end) < 4:
                self.p_end = '2020-01-01 12:00:00'
            self.stop_year = int(self.p_end[0:4])
            self.stop_month = int(self.p_end[5:7])
            self.stop_day = int(self.p_end[8:10])

            if p_unit != '':
                self.setval = 'Dag'
                if len(self.p_unit) > 1:
                    self.setval = self.p_unit

            print(f'self.url_fields = {self.url_fields}')
    #        gui.attributes('-alpha', 1.0)  # EM: maakt weer zichtbaar
            base_width = self.info_frame.winfo_width()
            print(f'WIDTH = {base_width}')
            self.fr_settings.configure(width=base_width)

    def go_back(self):
        self.controller.lastframe()

    def accept(self, mmode):
        # User pushed ready button
        # entered values are within the allowed range so prepare the call
        self.period_start = str(self.start_date.get_date())
        if mmode != 'date':
            self.period_start += ' '
            self.period_start += str(self.val_strt_hr.get())
            self.period_start += ':'
            self.period_start += str(self.val_strt_min.get())
            self.period_start += ':00'

        self.period_end = str(self.stop_date.get_date())
        if mmode != 'date':
            self.period_end += ' '
            self.period_end += str(self.val_end_hr.get())
            self.period_end += ':'
            self.period_end += str(self.val_strt_min.get())
            self.period_end += ':00'

        self.period_unit = self.unit_var.get()
        if len(self.period_unit):
            print(f'self.period_unit = {self.period_unit}')
            idx = gl.list_of_units_nl.index(self.period_unit)
            self.period_unit = gl.list_of_units_en[idx]
        print(f'self.period_start = {self.period_start}, '
              f'self.period_end = {self.period_end}, self.period_unit = {self.period_unit}')

        if not self.check_request(self.api_name,
                                  str(self.start_date.get_date()),
                                  str(self.stop_date.get_date()),
                                  self.period_unit):
            self.TopMessage(5000, 'Foutje', 'De ingevoerde waarden zijn in dit verzoek niet toegestaan')
            return
        else:
            self.TopMessage(5000, 'Foutje', 'De ingevoerde waarden zijn toegestaan')
            return
    # call saved settings

    def check_request(self, api_choice, strt_date, end_date, unit):
        # Validate user choices of 'energy', 'timeFrameEnergy','power','powerDetails','energyDetails'
        date_strt = datetime.strptime(strt_date, "%Y-%m-%d")
        date_end = datetime.strptime(end_date, "%Y-%m-%d")
        r = relativedelta.relativedelta(date_end, date_strt)
        pstart = {'year': date_strt.year,
                      'month': date_strt.month,
                      'day': date_strt.day}
        pend = {'year': date_end.year,
                      'month': date_end.month,
                      'day': date_end.day}
        print(pstart)
        print(pend)
        print(r.years, r.months, r.days)
        print(unit)
        retval = False
        print(f'api_choice = {api_choice}')
        if api_choice == 'energy':  #
            if unit in 'DAY':
                # Max 1 year
                if r.years + (r.months * 12) + r.days > 1:
                    # print(f"{unit} {pend['year']}>{pstart['year']} and{pend['month']}>{pstart['month']}")
                    retval = False
                else:
                    retval = True
            elif unit in ('QUARTER_OF_AN_HOUR', 'HOUR'):
                # Max 1 month
                print('Not defined yet')
                pass

            pass
        elif api_choice == 'timeFrameEnergy':
            # Max 1 year if timeUnit=DAY
            pass
        elif api_choice == 'power':
            # Max 1 month!!
            pass
        elif api_choice == 'powerDetails':
            # Max 1 month
            pass
        elif api_choice == 'energyDetails':
            # Max 1 year if timeUnit=DAY
            # Max 1 month if resolution higher
            # NO max if resolution = low (weekly, monthly, yearly)
            pass
        else:
            pass
        return retval

    def call_report(self):
        api_conn = CallApi

        content = api_conn.get_report(self, self.api_name, self.url_args)
        if len(content):
            pass

    def set_text(self, txt):
        pass
