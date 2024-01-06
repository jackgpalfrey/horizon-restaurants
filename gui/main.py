import tkinter as tk
from tkinter import ttk
from gui_lib import Page, PageManager

from Login import LoginPage, ChooseBranch
from City import CitiesPage
from api import API, URL, State


class App(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        root.geometry("675x400")
        root.title('Horizon Restaurants')
        root.resizable(0, 0)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=3)
        self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn', )

        notebook = ttk.Notebook(self, style='lefttab.TNotebook')
        notebook.pack(fill='both', expand=True)

        # create frames

        frame1 = CitiesPage(notebook)

        notebook.add(frame1, text='Cities')

        btn = tk.Button(self, text="Logout",
                        command=lambda: self.pages.goto("loggedout"))
        btn.pack()


if __name__ == "__main__":
    root = tk.Tk()
    main = PageManager(root)
    main.pack(side="top", fill="both", expand=True)

    main.add_page("loggedout", ChooseBranch)
    main.add_page("login", LoginPage)
    main.add_page("loggedin", App)

    main.goto("loggedout")

    root.mainloop()
