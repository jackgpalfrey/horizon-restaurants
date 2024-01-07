import tkinter as tk
from tkinter import ttk
from gui_lib import Page, PageManager

from Login import LoginPage, ChooseBranch
from City import CitiesPage
from MainPage import MainTab
from Staff import StaffPage
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
            role_id = user_data["data"]["role"]["id"]
            match role_id:
                case 1:
                    self.notebook.hide(2)

    def create_notebook_widget(self):
        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        self.notebook = ttk.Notebook(self, style='lefttab.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        # create frames

        frame1 = MainTab(self.notebook)
        frame2 = StaffPage(self.notebook)
        frame3 = CitiesPage(self.notebook)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        self.notebook.add(frame1, text='Home')
        self.notebook.add(frame2, text='Staff')
        self.notebook.add(frame3, text='Cities')

        btn = tk.Button(self, text="Logout",
                        command=lambda: self.pages.goto("loggedout"))
        btn.pack()

    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "Home":
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
