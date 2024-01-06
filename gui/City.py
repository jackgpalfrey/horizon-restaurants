from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State


class CitiesPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn', )

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        frame1 = ViewCities(notebook)

        notebook.add(frame1, text='View All Cities')


class ViewCities(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('city_name')

        tree = ttk.Treeview(self, columns=columns, show='headings')
        tree.heading('city_name', text='Cities')

        all_cities_res = API.post(f"{URL}/cities")
        all_cities = all_cities_res.json()
        for city in all_cities["data"]["cities"]:
            tree.insert('', 'end', values=(f"{city["name"]}"))

        tree.pack(fill='x', expand=True)
