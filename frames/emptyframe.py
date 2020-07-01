import tkinter as tk
from tkinter import ttk


class Empty(tk.Frame):
    def __init__(self, parent, controller):  # parent comes with desk_frame = Desk(self)
        tk.Frame.__init__(self, parent)

        self.controller = controller
        ttk.Label(self, text=f'Nagenoeg leeg frame in {__name__}').grid()
        # self.controller.geometry('1200x800')     # works not

    def set_text(self, txt):
        pass

