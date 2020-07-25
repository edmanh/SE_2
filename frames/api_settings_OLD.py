import tkinter as tk
from tkinter import ttk
from tkinter import font  as tkfont
from tkcalendar import DateEntry
from lib.functions import lineno
import lib.globals as gl
import lib.functions as funcs

class ApiSettings(ttk.Frame):

    def __init__(self, parent, controller):
        """ parent = Frame container,
            controller = class SeReporter() """
        super().__init__(parent)


        start = kwargs.get('start')
        if len(start) < 4:
            start = '2020-01-01 12:00:00'
        sjear = int(start[0:4])
        smonth = int(start[5:7])
        sday = int(start[8:10])
        end = kwargs.get('end')
        if len(end) < 4:
            end = '2020-01-01 12:00:00'
        ejear = int(end[0:4])
        emonth = int(end[5:7])
        eday = int(end[8:10])
        mode = kwargs.get('mode')
        gui.attributes('-alpha', 0.0)  # EM: zichtbaarheid, 0.0 = transparant




    def accept(mmode):
        gl.period_start = str(e_start_date.get_date())
        if mmode != 'date':
            gl.period_start += ' '
            gl.period_start += str(val_strt_hr.get())
            gl.period_start += ':'
            gl.period_start += str(val_strt_min.get())
            gl.period_start += ':00'

        gl.period_end = str(e_end_date.get_date())
        if mmode != 'date':
            gl.period_end += ' '
            gl.period_end += str(val_end_hr.get())
            gl.period_end += ':'
            gl.period_end += str(val_strt_min.get())
            gl.period_end += ':00'

        gl.period_unit = e_unit_var.get()
        gui.destroy()


        # ------------- Start building panel --------------
        bf = Frame(gui, width=600)
        bf.grid(row=0)

        titleframe = Frame(bf, bd=2, relief=FLAT)
        titleframe.grid(row=0)

        infoframe = LabelFrame(bf, text=' Aanwijzingen ', width=350, font=cnf.fa12, bd=2, relief=GROOVE)
        infoframe.grid(row=1, pady=(5, 0))

        strtframe = LabelFrame(bf, text=' Begin ', width=350, font=cnf.fa12, bd=2, relief=GROOVE)
        strtframe.grid(row=2)

        stpframe = LabelFrame(bf, text=' Eind ', width=350, font=cnf.fa12, bd=2, relief=GROOVE)
        stpframe.grid(row=3, sticky='ew')  # , pady=10

        titlelabel = Label(titleframe,
                           text=f'Vaststellen periode voor {kwargs.get("name")}',
                           font=cnf.fh12)
        titlelabel.grid(row=0, padx=5, pady=5)

        infotext = Text(infoframe, bg='#fffae3', height=3, width=16, font=cnf.fh12, bd=2, padx=5, pady=5)
        infotext.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=10)
        infotext.insert(END, kwargs['info'])

        e_start_date = DateEntry(strtframe, width=12, date_pattern='yyy-mm-dd', font=cnf.fa12,
                                 year=sjear, month=smonth, day=sday,
                                 background='darkblue', foreground='white')
        e_start_date.grid(row=0, column=0, padx=20, pady=20)

        e_end_date = DateEntry(stpframe, width=12, date_pattern='yyy-mm-dd', font=cnf.fh12,
                               year=ejear, month=emonth, day=eday,
                               background='darkblue', foreground='white')
        e_end_date.grid(row=2, column=0, padx=20, pady=20)

        val_strt_hr = StringVar()
        val_strt_min = StringVar()
        val_end_hr = StringVar()
        val_end_min = StringVar()

        if mode == 'date':
            # No start- and end time
            pass
        else:
            # Create start time entries
            e_start_time_hr = ttk.Combobox(strtframe,
                                           textvariable=val_strt_hr, values=gl.hrlist, font=cnf.fa12, width=2)
            e_start_time_hr.grid(row=0, column=1)
            e_start_time_hr.current(2)
            Label(strtframe, text=' : ', font=cnf.fa12).grid(row=0, column=2)
            e_start_time_min = ttk.Combobox(strtframe,
                                            textvariable=val_strt_min, values=gl.mnlist, font=cnf.fa12, width=2)
            e_start_time_min.grid(row=0, column=3, padx=(0, 20))
            e_start_time_min.current(0)

            # Create stop time entries
            e_end_time_hr = ttk.Combobox(stpframe, textvariable=val_end_hr, values=gl.hrlist, font=cnf.fa12, width=2)
            e_end_time_hr.grid(row=2, column=1)
            e_end_time_hr.current(16)
            Label(stpframe, text=' : ', font=cnf.fa12).grid(row=2, column=2)
            e_end_time_min = ttk.Combobox(stpframe,
                                          textvariable=val_end_min, values=gl.mnlist, font=cnf.fa12, width=2)
            e_end_time_min.grid(row=2, column=3, padx=(0, 20))
            e_end_time_min.current(0)

        if 'unit' in kwargs.keys():
            setval = 'Dag'
            if len(kwargs['unit']) > 1:
                setval = kwargs['unit']
            uframe = LabelFrame(bf, text='Interval', font=cnf.fa12)
            uframe.grid(row=4, padx=20, sticky=W)
            e_unit_var = StringVar()
            e_unit_var.set(setval)
            e_unit = OptionMenu(uframe, e_unit_var, *gl.list_of_units_nl)
            e_unit.grid(row=0, column=1, sticky=W)

        acceptbutton = Button(gui, text='Klaar', font=cnf.fa12, command=lambda: accept(mode))
        acceptbutton.grid(row=4, sticky=E, padx=20, pady=10)
        print(f'breedte = {gui.winfo_width()}')
        print(f'hoogte = {gui.winfo_height()}')


        center(gui)
        gui.attributes('-alpha', 1.0)  # EM: maakt weer zichtbaar
