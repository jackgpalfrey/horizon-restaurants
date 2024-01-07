from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk


class MainTab(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        label = ttk.Label(self, textvariable="Hi sisters!")
        label.pack()
