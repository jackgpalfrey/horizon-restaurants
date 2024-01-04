from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk


class ChooseBranch(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        dropdown = [
            "Branch"
        ]

        clicked = StringVar()
        clicked.set("Choose a Branch")

        drop = OptionMenu(self, clicked, *dropdown)
        drop.pack()

        btn = tk.Button(self, text="Choose Branch",
                        command=lambda: self.pages.goto("login"))
        btn.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)


class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is the login page")
        label.pack()
        self.create_widgets()

    def create_widgets(self):
        username = tk.StringVar()
        password = tk.StringVar()

        fields = {}  # dictionary
        fields['username_label'] = ttk.Label(self, text='Username:')
        fields['username'] = ttk.Entry(self, textvariable=username)
        fields['password_label'] = ttk.Label(self, text='Password:')
        fields['password'] = ttk.Entry(self, textvariable=password, show="*")

        for field in fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        btn = tk.Button(self, text="Login",
                        command=lambda: self.pages.goto("loggedin"))
        btn.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)
