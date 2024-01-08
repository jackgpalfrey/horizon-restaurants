# Author: Dina Hassanein (22066792)
from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import URL, API, State

branch_data = None


class ChooseBranch(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()
        self.drop = None

    def create_widgets(self):
        label = tk.Label(self, text="Please choose a branch")
        label.grid()

        self.all_branches_res = API.post(f"{URL}/branches")
        self.all_branches = self.all_branches_res.json()

    def on_show(self):
        if len(self.all_branches["data"]["branches"]) == 0:
            self.pages.goto("login")
            return

        State.is_ui_rendered = False

        if self.drop is None:
            self.dropdown = []

            global branch_data
            branch_data = {}
            for branch in self.all_branches["data"]["branches"]:
                self.dropdown.append(branch["name"])
                branch_data[branch["name"]] = branch["id"]

            global clicked
            clicked = StringVar()
            display_text = self.dropdown[0]
            clicked.set(display_text)
            self.drop = OptionMenu(self, clicked, *self.dropdown)
            self.drop.grid()

            def on_select():
                State.branch_id = branch_data[clicked.get()]
                self.pages.goto("login")

            btn = tk.Button(self, text="Choose Branch",
                            command=on_select)
            btn.grid()


class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        username_label = ttk.Label(self, text="Username:").grid(
            column=0, row=0, sticky=tk.W, padx=5, pady=5)
        username_entry = ttk.Entry(self, textvariable=self.username).grid(
            column=1, row=0, sticky=tk.W, padx=5, pady=5)
        password_label = ttk.Label(self, text="Password:").grid(
            column=0, row=1, sticky=tk.W, padx=5, pady=5)
        password_entry = ttk.Entry(
            self, textvariable=self.password, show="*").grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

        btn = tk.Button(self, text="Login", command=self.handle_input)
        btn.grid(column=0, row=2, sticky=tk.W, padx=5)
        self.label = Label(self, text="")
        self.label.grid(column=1, row=2)

    def handle_input(self):
        if self.username.get() != "admin":
            branch_id = branch_data[clicked.get()]
            branch_users_res = API.post(f"{URL}/branches/{branch_id}/users")
            branch_users = branch_users_res.json()
            for user in branch_users["data"]["users"]:
                did_find = user["username"] == self.username.get()
                if did_find:
                    break
            if not did_find:
                self.label["text"] = "This user doesn't work at this branch."
                return
        login_data = {"username": self.username.get(
        ), "password": self.password.get()}
        State.is_ui_rendered = False
        login = API.post(f"{URL}/login", json=login_data)
        match login.status_code:
            case 200:
                self.label["text"] = ""
                State.username = login_data["username"]
                self.username.set("")
                self.password.set("")
                self.pages.goto("loggedin")
            case 401:
                self.label["text"] = "Invalid Credentials"
