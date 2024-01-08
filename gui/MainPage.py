from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk


class MainTab(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        label = ttk.Label(self, textvariable="Main Page")
        label.pack()

        # no branches created. to be able to select a branch and login to it as staff member,
        # admin acount must create branch first.
