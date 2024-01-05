from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import URL, API, State


class ChooseBranch(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Please choose a branch")
        label.grid()

        dropdown = []

        all_branches_res = API.post(f"{URL}/branches")
        all_branches = all_branches_res.json()

        global branch_data
        branch_data = {}
        for branch in all_branches["data"]["branches"]:
            dropdown.append(branch["name"])
            data = {branch["name"]: branch["id"]}
            branch_data.update(data)

        global clicked
        clicked = StringVar()
        display_text = dropdown[0]
        clicked.set(display_text)
        drop = OptionMenu(self, clicked, *dropdown)
        drop.grid()
        btn = tk.Button(self, text="Choose Branch",
                        command=lambda: self.pages.goto("login"))
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
        branch_id = branch_data[clicked.get()]
        branch_users_res = API.post(f"{URL}/branches/{branch_id}/users")
        branch_users = branch_users_res.json()

        if self.username.get() != "admin":
            for user in branch_users["data"]["users"]:
                if user["username"] == self.username.get():
                    break
                print("This user doesn't work at this branch.")

        login_data = {"username": self.username.get(
        ), "password": self.password.get()}
        login = API.post(f"{URL}/login", json=login_data)
        match login.status_code:
            case 200:
                self.label["text"] = ""
                self.pages.goto("loggedin")
            case 401:
                self.label["text"] = "Invalid Credentials"
