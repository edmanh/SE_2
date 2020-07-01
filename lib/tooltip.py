
from tkinter import ttk
from tkinter import *


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        # 'widget' is the id of a connecting widget
        # 'text' is the heelp text to present
        self.waittime = 500     # milliseconds
        self.wraplength = 180   # pixels
        self.widget = widget

        self.text = text
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.leave)
        self.widget.bind('<ButtonPress>', self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        idnow = self.id
        self.id = None
        if idnow:
            self.widget.after_cancel(idnow)

    def showtip(self, event=None):
        x, y, cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry('+%d+%d' % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                      background='#ffffff', relief='ridge', borderwidth=4,
                      wraplength=self.wraplength)
        label.pack(ipadx=4, ipady=4)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
#  ================ end of class CreateToolTip() ==============
