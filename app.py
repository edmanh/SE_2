import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import logging
from frames import Desk, Empty, ByeBye, ReportTypeMenu, ViewReport, GetHistReport, SetNewReport
import lib.config as cnf
from lib.functions import lineno
from lib.functions import set_dpi_awareness
import lib.globals as gl

# Start logging
# selogger.info('\n\n\t-------------- Start logging --------------')
# selogger.info(f'cwd = {cwd}')


set_dpi_awareness()

PANEL_BACKGROUND = '#ffefd8'  #
PANEL_FOREGROUND = '#fffae3'  #
PANEL_LABEL_TEXT = '#000'
PANEL_LABEL_BACKGROUND = '#ffbc46'
REMARK_TEXT = '#000'
REMARK_BACKGROUND = '#efc396'
MENU_BUTTON_TEXT = '#ffffff'
MENU_BUTTON_BACKGROUND = 'black'



class SeReporter(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('SolarEdge Reporter')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold', slant='italic')

        self.message = tk.StringVar(value='Empty')  # Var to pass messages
        self.trigger_show_rap = tk.IntVar(value=0)
        self.framehist = list()
        self.tmp_file = False
        self.report_type = ''

        # === Start of styling ===
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            'Panel.TFrame',
            background=PANEL_BACKGROUND,
            )

        style.configure(
            'TestPanel.TFrame',
            background='#18578a',
            )

        style.configure(
            'Panel.TLabelframe',
            background=PANEL_BACKGROUND,
            bd=4
            )

        style.configure(
            'PanelLabel.TLabel',
            background=PANEL_LABEL_BACKGROUND,
            foreground=PANEL_LABEL_TEXT,
            relief='ridge',
            font='Helvetica 16',
            borderwidth=5,
            padding=10,
            anchor='CENTER'
            )

        style.configure(
            'PanelHint.TLabel',
            background=REMARK_BACKGROUND,
            foreground=REMARK_TEXT,
            relief='groove',
            font='Helvetica 12',
            borderwidth=4,
            padding=10
            )

        style.configure(
            "StatusText.TLabel",
            background=REMARK_BACKGROUND,
            foreground=REMARK_TEXT,
            font=cnf.fh12,
            borderwidth=3,
            relief='sunken',
            padding=5
            )

        style.configure(
            "MenuButton.TButton",
            background=MENU_BUTTON_BACKGROUND,
            foreground=MENU_BUTTON_TEXT,
            font='Helvetica 11',
            padding=10
            )

        style.configure(
            "ChoiceButton.TButton",
            background='#cfb290',
            foreground='#8d441d',
            font='Helvetica 11',
            padding=10
            )

        style.map(
            "MenuButton.TButton",
            background=[("active", MENU_BUTTON_BACKGROUND), #  black
                        ("disabled", MENU_BUTTON_TEXT)],     #
            foreground=[("disabled", MENU_BUTTON_BACKGROUND),
                        ("active", MENU_BUTTON_TEXT)]
            )
        ## === End of styling ===

        # Prepare global data
        print(f'Prepare globaly used dicts')
        all_args = dict()  # Holds api args
        all_info = dict()  # Holds api info
        all_titles = dict()  # Holds choice button titles
        for app, attribs in cnf.api_config.items():
            all_args[app] = attribs['args']
            all_info[app] = attribs['info']
            all_titles[app] = attribs['args'][0]  # App Button Titles

        print(all_titles)

        container = tk.Frame(self, bg='#808080', bd=5)  # background = grey
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Desk, ReportTypeMenu, ViewReport, Empty, ByeBye, GetHistReport, SetNewReport):
            page_name = F.__name__
            print(f'Loaded module {page_name}')
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('Desk')

        # self.get_widget_attributes(self.container)  # .container

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        self.set_title(page_name)
        self.framehist.append(page_name)
        frame = self.frames[page_name]
        print(f'geo = {frame.geo}')
        if 'x' in frame.geo:
            self.geometry(frame.geo)
        if self.message:
            msg = self.message
            frame.set_text(msg)
        print(f'>>>Start showing frame - {page_name} -')
        frame.tkraise()
        if hasattr(frame, 'go'):
            print(f'{page_name} has go as attr')
            frame.go()
        else:
            print(f'{page_name} has NO attr named go')
        return True

    def lastframe(self):
        print(f'Called go_back from {self.framehist[-1]}')
        self.framehist.pop()
        if len(self.framehist) > 0:
            self.show_frame(self.framehist.pop())

    def set_title(self, page):
        self.title(f'SolarEdge reporter - {page}')

    @staticmethod
    def get_widget_attributes(widget):
        print(f'>>>>> Show widget info of {widget}')
        all_widgets = widget.winfo_children()  # self.f1.winfo_children()
        for widg in all_widgets:
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            keys = widg.keys()
            for key in keys:
                print("Attribute: {:<20}".format(key), end=' ')
                value = widg[key]
                vtype = type(value)
                print('Type: {:<30} Value: {}'.format(str(vtype), value))

    def set_message(self, msg):
        self.message = msg
        print(f'{__name__}-{lineno()} Val = {self.message}')

    def close_app(self):
        print(f'{__name__}, {lineno()}: app closed')
        self.destroy()

    def set_trigger(self, trigger):
        if trigger == 'show':
            self.trigger_show_rap = 1
        if trigger == 'newReport':
            pass
        return


if __name__ == "__main__":
    app = SeReporter()
#    app.get_widget_attributes(app)
    app.wait_window(SetNewReport.db)
    app.mainloop()
