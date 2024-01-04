"""Module for managing multiple pages together."""
import tkinter as tk
from .Page import Page


class PageManager(tk.Frame):
    """
    Class for managing multiple pages.

    Add new pages with add_page() and toggle between pages with goto()
    """

    def __init__(self, *args, **kwargs):
        """Provide init a widget, normally tk.Tk as it's parent."""
        self._pages: dict[str, Page] = {}
        self._active_page: Page | None = None

        tk.Frame.__init__(self, *args, **kwargs)

    def goto(self, page_id: str):
        """Switch from current page to another."""
        if self._active_page is not None:
            self._active_page.hide()

        page = self._pages.get(page_id)
        self._active_page = page

        if self._active_page is not None:
            self._active_page.show()

    def add_page(self, page_id: str, page: type[Page]):
        """Add new page to PageManager."""
        self._pages[page_id] = page(self)
