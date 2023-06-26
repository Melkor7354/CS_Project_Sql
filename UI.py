from tkinter import *
import tkinter as tk
import colour_scheme as c


class UI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.config(background=c.primary, )
