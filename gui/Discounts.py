from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State


class DiscountsPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = DiscountsHomePage(notebook)
        self.frame2 = ViewDiscounts(notebook)
        self.frame3 = CreateDiscount(notebook)
        self.frame4 = UpdateDiscount(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='Home')
        notebook.add(self.frame2, text='View All Discounts')
        notebook.add(self.frame3, text='Create Discount')
        notebook.add(self.frame4, text='Update Discount')

    def on_tab_selected(self, event):
        # ref: https://www.homeandlearn.uk/python-database-form-tabs3.html
        if State.username is None:
            return
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Discounts":
            self.frame2.load_records()
        if tab_text == "Create Discount":
            self.frame2.load_records()
        if tab_text == "Update Discount":
            self.frame2.load_records()


class ViewDiscounts(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('multiplier', 'description')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('multiplier', text='Multiplier')
        self.tree.heading('description', text='Description')

        delete_button = ttk.Button(
            self, text='Delete All Records', command=self.delete_all_records)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def load_records(self):
        if State.branch_id is None:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        branch_id = State.branch_id
        branch_discounts_res = API.post(
            f"{URL}/branches/{branch_id}/discounts")
        print(branch_discounts_res)
        branch_discounts = branch_discounts_res.json()
        print(branch_discounts, "!!!!")

        global discount_data
        discount_data = {}
        # category_data = {}

        for discount in branch_discounts["data"]["discounts"]:
            self.tree.insert('', 'end', values=(
                discount["multiplier"], discount["description"]))
            discount_data[discount["multiplier"]] = discount["id"]

        self.tree.pack(fill='x', expand=True)

    def delete_all_records(self):
        branch_id = State.branch_id
        for record in discount_data:
            res = API.post(
                f"{URL}/branches/{branch_id}/discounts/{discount_data[record]}/delete")
        self.load_records()


class DiscountsHomePage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ttk.Label(self, text="Discounts Management Page")
        label.pack()


class CreateDiscount(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.multipler = tk.DoubleVar()
        self.description = tk.StringVar()

        self.fields = {}

        self.fields['item_name_label'] = ttk.Label(self, text='Multiplier:')
        self.fields['item_name'] = ttk.Entry(self, textvariable=self.multipler)
        self.fields['description_label'] = ttk.Label(self, text='Description:')
        self.fields['description'] = ttk.Entry(
            self, textvariable=self.description)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="", wraplength=370)
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        create_button = ttk.Button(
            self, text='Create Discount ', command=self.add_record)
        create_button.pack(anchor=tk.E, padx=5, pady=5)

    def add_record(self):
        for multiplier in discount_data:
            if multiplier == self.multipler.get():
                self.fields['message']["text"] = "This discount already exists."
                return
        branch_id = State.branch_id
        if branch_id is None:
            self.fields['message']["text"] = "Current user isn't logged into or assigned a branch, Choose a branch on login first to create branch items"
            return
        self.fields['message']["text"] = ""
        discount_info = {"multiplier": self.multipler.get(
        ), "description": self.description.get()}
        branch_id = State.branch_id
        create = API.post(
            f"{URL}/branches/{branch_id}/discounts/create", json=discount_info)
        print(create.json())
        match create.status_code:
            case 200:
                self.fields['message']["text"] = "Discount Created Successfully"
            case 400 | 409 | 401:
                self.fields['message']["text"] = create.json()["message"]


class UpdateDiscount(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.multiplier = tk.DoubleVar()

        self.fields = {}

        self.fields['item_name_label'] = ttk.Label(
            self, text='Find Discount By Multiplier:')
        self.fields['item_name'] = ttk.Entry(
            self, textvariable=self.multiplier)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        delete_button = ttk.Button(
            self, text='Delete Discount ', command=self.delete_record)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def delete_record(self):
        multiplier = self.multiplier.get()
        multiplier_id = discount_data[multiplier]
        branch_id = State.branch_id
        for record in discount_data:
            if multiplier == record:
                delete_item = API.post(
                    f"{URL}/branches/{branch_id}/discounts/{multiplier_id}/delete")
                break
        match delete_item.status_code:
            case 200:
                self.fields['message']["text"] = "Menu Item Deleted Successfully"
