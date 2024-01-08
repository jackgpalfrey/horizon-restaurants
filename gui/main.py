# Author: Dina Hassanein (22066792)
import tkinter as tk
from tkinter import ttk
from gui_lib import Page, PageManager

from MainPage import MainTab
from Login import LoginPage, ChooseBranch
from Staff import StaffPage
from City import CitiesPage
from Branch import BranchesPage
from Inventory import InventoryPage
from Table import TablesPage
from Menu import MenuPage
from Discounts import DiscountsPage
from Reservations import ReservationsPage
from api import API, URL, State


class App(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        root.geometry("1005x400")
        root.title('Horizon Restaurants')
        root.resizable(1, 1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=3)
        self.create_notebook_widget()

    def on_show(self):
        self.user_view()

    def user_view(self):
        user = State.username
        user_data_res = API.post(f"{URL}/users/{user}", json=user)
        user_data = user_data_res.json()
        if user_data["success"]:
            try:
                self.notebook.forget(0)
                self.notebook.forget(1)
                self.notebook.forget(2)
                self.notebook.forget(3)
                self.notebook.forget(4)
                self.notebook.forget(5)
                self.notebook.forget(6)
                self.notebook.forget(7)
                self.notebook.forget(8)
            except Exception as e:
                pass

            role_id = user_data["data"]["role"]["id"]

            match role_id:
                case 0:
                    self.notebook.add(self.frame1, text='Home')
                    self.notebook.add(self.frame7, text='Menu')
                    self.notebook.add(self.frame8, text='Discounts')
                case 1:
                    self.notebook.add(self.frame1, text='Home')
                    self.notebook.add(self.frame7, text='Menu')
                    self.notebook.add(self.frame8, text='Discounts')
                    self.notebook.add(self.frame9, text='Reservations')
                case 2:
                    self.notebook.add(self.frame1, text='Home')
                    self.notebook.add(self.frame7, text='Menu')
                    self.notebook.add(self.frame5, text='Inventory')
                    self.notebook.add(self.frame8, text='Discounts')
                case 3:
                    self.notebook.add(self.frame1, text='Home')
                    self.notebook.add(self.frame7, text='Menu')
                    self.notebook.add(self.frame5, text='Inventory')
                    self.notebook.add(self.frame8, text='Discounts')
                case 4:
                    self.notebook.add(self.frame1, text='Home')
                    self.notebook.add(self.frame3, text='Cities')
                    self.notebook.add(self.frame4, text='Branches')
                    self.notebook.add(self.frame5, text='Inventory')
                    self.notebook.add(self.frame6, text='Tables')
                    self.notebook.add(self.frame7, text='Menu')
                    self.notebook.add(self.frame8, text='Discounts')
                    self.notebook.add(self.frame9, text='Reservations')
                case 99:
                    self.notebook.add(self.frame1, text='Home')
                    self.notebook.add(self.frame2, text='Staff')
                    self.notebook.add(self.frame3, text='Cities')
                    self.notebook.add(self.frame4, text='Branches')
                    self.notebook.add(self.frame5, text='Inventory')
                    self.notebook.add(self.frame6, text='Tables')
                    self.notebook.add(self.frame7, text='Menu')
                    self.notebook.add(self.frame8, text='Discounts')
                    self.notebook.add(self.frame9, text='Reservations')
        State.is_ui_rendered = True

    def create_notebook_widget(self):
        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        self.notebook = ttk.Notebook(self, style='lefttab.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        # create frames

        self.frame1 = MainTab(self.notebook)
        self.frame2 = StaffPage(self.notebook)
        self.frame3 = CitiesPage(self.notebook)
        self.frame4 = BranchesPage(self.notebook)
        self.frame5 = InventoryPage(self.notebook)
        self.frame6 = TablesPage(self.notebook)
        self.frame7 = MenuPage(self.notebook)
        self.frame8 = DiscountsPage(self.notebook)
        self.frame9 = ReservationsPage(self.notebook)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        btn = tk.Button(self, text="Logout",
                        command=lambda: self.pages.goto("loggedout"))
        btn.pack()

    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if not State.is_ui_rendered:
            self.user_view()


if __name__ == "__main__":
    root = tk.Tk()
    main = PageManager(root)
    main.pack(side="top", fill="both", expand=True)

    main.add_page("loggedout", ChooseBranch)
    main.add_page("login", LoginPage)
    main.add_page("loggedin", App)

    main.goto("loggedout")

    root.mainloop()
