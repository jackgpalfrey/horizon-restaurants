import tkinter as tk
from gui_lib import Page, PageManager

from Login import LoginPage


class App(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        root.geometry("675x300")
        root.title('Horizon Restaurants')
        root.resizable(0, 0)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=3)

        label = tk.Label(self, text="This is the main page")
        label.pack()

        btn = tk.Button(self, text="Logout",
                        command=lambda: self.pages.goto("loggedout"))
        btn.pack()


if __name__ == "__main__":
    root = tk.Tk()
    main = PageManager(root)
    main.pack(side="top", fill="both", expand=True)

    main.add_page("loggedout", LoginPage)
    main.add_page("loggedin", App)

    main.goto("loggedout")

    root.mainloop()
