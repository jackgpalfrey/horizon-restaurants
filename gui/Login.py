from gui_lib import Page
import tkinter as tk


class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is the login page")
        label.pack()

        btn = tk.Button(self, text="Login",
                        command=lambda: self.pages.goto("loggedin"))
        btn.pack()
