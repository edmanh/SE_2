"""

"""
from datetime import datetime
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
from lib.dialogbox import DialogBox
set_dpi_awareness()
api = gl.MyApi


class SetNewReport(ttk.Frame):
    geo = '600x800'

    def __init__(self, parent, controller):
        """ parent = Frame container,
            controller = class SeReporter() """
        super().__init__(parent)

        self.controller = controller
        self.parent = parent
        gl.next_step = 'empty'
        self.url_fields = []
        self.titel_var = tk.StringVar()
        self.choice_var = tk.StringVar()
        self.protocol_var = tk.StringVar()
        self.val_strt_hr = tk.StringVar()
        self.val_strt_min = tk.StringVar()
        self.val_end_hr = tk.StringVar()
        self.val_end_min = tk.StringVar()

        # periode definitions
        self.period_start = ''
        self.period_end = ''
        self.period_unit = ''
        self.start_it = datetime.now()
        self.stop_it = func.add_one_month(datetime.now())

        # accept value
        self.p_start = ''
        self.p_stop = ''
        self.p_mode = ''
        self.p_unit = ''

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
                               text=' Rapport ....',
                               style='PanelLabel.TLabel',
                               width=40,  # Width in chars
                               anchor=tk.CENTER)
        page_label.grid(row=0, column=0, pady=(0, 5))

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
                                    #  year=self.strt_year, month=self.strt_month, day=self.strt_day,
                                    background='#0000ff', foreground='white')
        self.start_date.grid(row=0, column=0, padx=20, pady=10)
        self.start_date.set_date(self.start_it)
        #        std_width = self.fr_strt_date.winfo_width()
        # right = stop date
        fr_stop_date_label = tk.Label(self.fr_settings, text=' Stopdatum ', font=cnf.fa12, fg='black', bg='#ffefd8')
        self.fr_stop_date = ttk.LabelFrame(self.fr_settings, text=' ', width=175, height=80,
                                           labelwidget=fr_stop_date_label,
                                           style='Panel.TFrame',
                                           relief=tk.GROOVE)
        self.stop_date = DateEntry(self.fr_stop_date, width=12, date_pattern='yyy-mm-dd', font=cnf.fh12,
                                  #  year=self.stop_year, month=self.stop_month, day=self.stop_day,
                                  background='blue', foreground='white')
        self.stop_date.grid(row=0, column=1, padx=20, pady=10)
        self.stop_date.set_date(self.stop_it)

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
        self.unit_var.set(gl.list_of_units_nl[0])
        self.unit = ttk.OptionMenu(self.fr_unit, self.unit_var, *gl.list_of_units_nl,
                                   command=lambda x: self.set_time_unit(x))  # in original self was forwarded also
        self.unit_var.set(gl.list_of_units_nl[0])
        self.unit['menu'].configure(font=cnf.fa12)
        self.unit.configure(style='ChoiceButton.TButton')
        self.unit.grid(row=0, column=0, pady=(10, 10), padx=(20, 10))  # , padx=20, pady=10, sticky='E'
        self.fr_unit.grid(row=2, column=1, pady=(10, 10), padx=(10, 10))
        self.fr_unit.grid_propagate(0)

        self.acceptbutton = tk.Button(self.inside_frame, text='Verder',
                                 background='black', foreground='white',
                                 width=20, height=2, font=cnf.fa12,
                                 command=lambda: self.accept())
        self.acceptbutton.grid(row=6, column=0, sticky='E', padx=0, pady=20)

        backbutton = tk.Button(self.inside_frame, text='Terug',
                                 background='black', foreground='white',
                                 width=20, height=2, font=cnf.fa12,
                                 command=lambda: self.go_back())
        backbutton.grid(row=6, column=0, sticky='W', padx=0, pady=20)

    @staticmethod
    def set_time_unit(val):
        # For future improvements only
        print(f'returned val: {val}')
        pass

    def go(self):
        """
        User has chosen for a new report of a particular type
        Hide or show widgets dependent on api.name
        and get the right start values
        (from history database or defaults) into the widgets.
        :return:
        """

        #  api.name = self.parent.report_type
        self.titel_var.set(f' Rapportperiode samenstellen en rapport opvragen ')
        self.choice_var.set(f' Raportkeuze = "{cnf.all_titles.get(api.name)}"')
        self.protocol_var.set(f' Protocolnaam = "{api.name}"')
        # Get values to complete the arg list
        api_args = cnf.all_args[api.name][1:]  # args needed for the choosen api, skip translated title
        api.num_args = len(api_args)
        selogger.info(
            f'Gekozen titel: {cnf.all_titles[api.name]}, '
            f'de api naam is {api.name}, aantal args = {api.num_args}')

        self.infotext.delete('1.0', tk.END)
        self.infotext.insert(tk.END, cnf.api_config[api.name]['info'])
        print(f'{__name__}-{lineno()}: cnf.all_args[my.name] = {cnf.all_args[api.name]}')
        print(f'{__name__}-{lineno()}: api.num_args = {api.num_args}')
        #  print(cnf.api_config[api.name]['info'])
        if api.num_args == 0:
            # Requests without period definitions
            self.fr_unit.grid_remove()
            self.fr_strt_date.grid_remove()
            self.fr_stop_date.grid_remove()
            self.fr_strt_time.grid_remove()
            self.fr_stop_time.grid_remove()
            self.fr_settings.grid_remove()
        else:
            # Requests with date and/or date-time definitions
            self.fr_settings.grid(row=2, padx=20, pady=10)
            api.url_args.clear()  # in case user chooses new report type
            #  Possible arguments are: startDate + endDate OR startTime + endTime AND OPTIONAL timeUnit
            for next_arg in api_args:
                if next_arg == 'startDate':
                    # Set both date entries visible
                    self.fr_strt_date.grid(row=0, column=0, sticky='W', pady=(10, 10), padx=(10, 10))
                    self.fr_stop_date.grid(row=0, column=1, sticky='E', pady=(10, 10), padx=(10, 10))
                    api.url_args['startDate'] = ''
                    api.url_args['endDate'] = ''
                elif next_arg == 'startTime':
                    # Set both date + time entries visible
                    self.fr_strt_date.grid(row=0, column=0, sticky='W', pady=(10, 10), padx=(10, 10))
                    self.fr_stop_date.grid(row=0, column=1, sticky='E', pady=(10, 10), padx=(10, 10))
                    self.fr_strt_time.grid(row=1, column=0, sticky='W', pady=(10, 10), padx=(10, 0))
                    self.fr_stop_time.grid(row=1, column=1, sticky='E', pady=(10, 10), padx=(10, 10))
                    api.url_args['startTime'] = ''
                    api.url_args['endTime'] = ''
                elif next_arg in 'timeUnit':
                    # Set interval choice visible
                    self.fr_unit.grid(row=2, column=1, pady=(10, 10), padx=(10, 10))
                    api.url_args['timeUnit'] = ''

            # Fill widgets with last saved values
            arg_db_values = func.get_api_values(api.name)  # database action
            if 'startDate' in arg_db_values:
                if len(arg_db_values['startDate']):
                    self.start_date.set_date(arg_db_values['startDate'])
            if 'endDate' in arg_db_values:
                if len(arg_db_values['endDate']):
                    self.stop_date.set_date(arg_db_values['endDate'])

            if 'timeUnit' in api_args:
                p_unit = arg_db_values['timeUnit']
                self.url_fields.append('timeUnit')
            else:
                p_unit = ''
                self.fr_unit.grid_forget()
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

            # self.p_start = '2020-01-01 12:00:00'  # api compatible yyyy-mm-dd (and if time defined) hh:mm:ss
            # self.p_end = '2020-01-01 12:00:00'  # api compatible yyyy-mm-dd (and if time defined) hh:mm:ss

            if p_unit != '':
                self.unit_var.set('Dag')
                if len(self.p_unit) > 1:
                    self.unit_var.set(self.p_unit)

            print(lineno(), f'self.url_fields = {self.url_fields}')
            base_width = self.info_frame.winfo_width()
            self.fr_settings.configure(width=base_width)
        print(f"Var's in {__name__}: {dir()}")

    def go_back(self):
        self.controller.lastframe()

    def accept(self):
        # User pushed ready button
        if api.num_args == 0:
            self.controller.show_frame('GetNewReport')
            return
        # entered values must be api formatted and checked
        self.period_start = str(self.start_date.get_date())
        if self.p_mode != 'date':
            self.period_start += ' '
            self.period_start += str(self.val_strt_hr.get())
            self.period_start += ':'
            self.period_start += str(self.val_strt_min.get())
            self.period_start += ':00'

        self.period_end = str(self.stop_date.get_date())
        if self.p_mode != 'date':
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
        print(lineno(), f'self.period_start = {self.period_start}, '
              f'self.period_end = {self.period_end}, \nself.period_unit = {self.period_unit}')

        if not self.check_request(api.name,
                                  str(self.period_start),
                                  str(self.period_end),
                                  self.period_unit):
            TopMessage(cnf.wfquit, 'Foutje', 'De ingevoerde waarden in dit verzoek zijn niet toegestaan')
            return
        else:
            dp = dict()
            dp.clear()
            dp['title'] = 'Vraagje ..'
            dp['message'] = 'De ingevoerde waarden zijn toegestaan dus ...'
            dp['deny'] = 'Terug'
            dp['accept'] = 'OK, Doorgaan'
            self.call_dialog(**dp)
            if gl.next_step == 'no action':
                return
            if api.num_args > 0:
                # Ask for saving (modified) parameters
                dp.clear()
                dp['title'] = 'Nog een vraagje ..'
                dp['message'] = 'Instellingen eerst opslaan (in database) als nieuwe basiswaarde?'
                dp['deny'] = 'Terug'
                dp['accept'] = 'Opslaan graag'
                self.call_dialog(**dp)
                if gl.next_step == 'no action':
                    return
                # Save new values in database
                print(f'{__name__}-{lineno()}: api.url_args = {api.url_args}')
                query = 'UPDATE settings SET '
                for name in api.url_args:
                    val = ''
                    if name == 'timeUnit':
                        val = self.period_unit
                        if val in gl.list_of_units_en:
                            val = gl.list_of_units_nl[gl.list_of_units_en.index(val)]
                    elif name in ('startTime', 'startDate'):
                        val = self.period_start
                    elif name in ('endTime', 'endDate'):
                        val = self.period_end
                    query += f'{name} = "{val}", '
                query = query[0:-2]  # remove last comma-space
                query += f' WHERE name = "{api.name}"'
                print(lineno(), f'query = {query}')
                rows = func.actdb.exec_update(query)
                if rows > 0:
                    selogger.info('Laatste instellingen opgeslagen.')
            # self.controller.set_trigger('newReport')
            self.controller.show_frame('GetNewReport')

        #   =========================================================================================

    @staticmethod
    def check_request(api_choice, strt_moment, end_moment, unit):
        """ Validate user choices of 'energy', 'timeFrameEnergy','power','powerDetails','energyDetails' """
        ret_val = False
        # Checking settings per api
        d = dict()
        d['strt'] = strt_moment
        d['end'] = end_moment
        if api_choice == 'energy':                                  # Periodeopbrengst in detail
            if unit in 'DAY':
                # Max 1 year
                d['delta'] = 'year'
                res = func.check_periode_limit(None, **d)
                if res == 1:
                    msg = 'De gekozen periode is te lang voor de waarden per: dag'
                    TopMessage(cnf.wfquit, 'Foutje', msg)
                    ret_val = False
                elif res == -1:
                    msg = 'De start- en einddatums zijn omgedraaid'
                    TopMessage(cnf.wfquit, 'Foutje', msg)
                    ret_val = False
                else:
                    ret_val = True
            elif unit in ('QUARTER_OF_AN_HOUR', 'HOUR'):
                # Max 1 month
                d['delta'] = 'month'
                res = func.check_periode_limit(None, **d)
                if res == 1:
                    msg = 'De gekozen periode is te lang bij waarden per: uur of kwartier'
                    TopMessage(cnf.wfquit, 'Foutje', msg)
                    ret_val = False
                elif res == -1:
                    msg = 'De start- en einddatums zijn omgedraaid'
                    TopMessage(cnf.wfquit, 'Foutje', msg)
                    ret_val = False
                else:
                    ret_val = True
            else:
                ret_val = True

        elif api_choice == 'timeFrameEnergy':                       # Periodeopbrengst samenvatting
            # Total over given period, no limits
            if strt_moment == end_moment:
                msg = 'Dezelfde dag en zonder tijden is niet logisch, ' \
                      'probeer dan liever \n"Periodeopbrengst in detail"\n' \
                      'want daar kun je ook de tijd aangeven'
                TopMessage(cnf.wfquit, 'Foutje', msg)
                ret_val = False
            else:
                d['delta'] = ''
                res = func.check_periode_limit(None, **d)
                if res == -1:
                    msg = 'Stopdatum dient ná Startdatum te liggen'
                    TopMessage(cnf.wfquit, 'Foutje', msg)
                    ret_val = False
                else:
                    ret_val = True
        elif api_choice == 'power':                                 # Periodeopbrengst per kwartier
            # Max 1 month!!
            d['delta'] = 'month'
            res = func.check_periode_limit(None, **d)
            if res == 1:
                msg = 'Dit rapport levert kwartierwaarden en mag daarom niet langer zijn dan één maand\n' \
                      'Tip: let op de tijden!'
                TopMessage(cnf.wfquit, 'Foutje', msg)
                ret_val = False
            elif res == -1:
                msg = 'Stopdatum (plus tijd) dient ná Startdatum (plus tijd) te liggen'
                TopMessage(cnf.wfquit, 'Foutje', msg)
                ret_val = False
            else:
                ret_val = True
        elif api_choice in ('overview',      # Overzicht
                            'details',       # Installatie details
                            'dataPeriod',    # start- and enddate of installation
                            'inventory',     # List of technical installation details
                            'envBenefits'):  # Environment benefits like CO2
            ret_val = True
        else:
            pass
        return ret_val

    def call_report(self):
        api_conn = CallApi
        content = api_conn.get_report(api.name, api.url_args)
        if len(content):
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
