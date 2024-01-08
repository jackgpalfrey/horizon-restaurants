from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State


class MenuPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = MenuHomePage(notebook)
        self.frame2 = ViewItems(notebook)
        self.frame3 = CreateItem(notebook)
        self.frame4 = UpdateItem(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='Home')
        notebook.add(self.frame2, text='View All Menu Items')
        notebook.add(self.frame3, text='Create Menu Item')
        notebook.add(self.frame4, text='Update Menu Item')

    def on_tab_selected(self, event):
        # ref: https://www.homeandlearn.uk/python-database-form-tabs3.html
        if State.username is None:
            return
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Menu Items":
            self.frame2.load_records()
        if tab_text == "Create Menu Item":
            self.frame2.load_records()
        if tab_text == "Update Menu Item":
            self.frame2.load_records()


class ViewItems(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('item_name', 'price', 'description', 'category')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('item_name', text='Item Name')
        self.tree.heading('price', text='Price')
        self.tree.heading('description', text='Description')
        self.tree.heading('category', text='Category')

        delete_button = ttk.Button(
            self, text='Delete All Records', command=self.delete_all_records)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def load_records(self):
        if State.branch_id is None:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        branch_id = State.branch_id
        branch_menu_res = API.post(
            f"{URL}/branches/{branch_id}/menu")
        branch_menu = branch_menu_res.json()
        print(branch_menu, "!!!!")

        global menu_data
        menu_data = {}
        # category_data = {}

        for item in branch_menu["data"]["menu"]:
            self.tree.insert('', 'end', values=(
                item["name"], item["price"], item["description"], item["category"]["name"]))
            menu_data[item["name"]] = item["id"]

        self.tree.pack(fill='x', expand=True)

    def delete_all_records(self):
        branch_id = State.branch_id
        for record in menu_data:
            res = API.post(
                f"{URL}/branches/{branch_id}/menu/{menu_data[record]}/delete")
        self.load_records()


class MenuHomePage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ttk.Label(self, text="Menu Management Page")
        label.pack()


class CreateItem(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.item_name = tk.StringVar()
        # self.category = tk.StringVar()
        self.price = tk.DoubleVar()
        self.description = tk.StringVar()

        self.fields = {}

        self.fields['item_name_label'] = ttk.Label(self, text='Item Name:')
        self.fields['item_name'] = ttk.Entry(self, textvariable=self.item_name)
        # self.fields['category_label'] = ttk.Label(self, text='Category:')
        # self.fields['category'] = ttk.Entry(self, textvariable=self.category)
        self.fields['price_label'] = ttk.Label(self, text='Price:')
        self.fields['price'] = ttk.Entry(self, textvariable=self.price)
        self.fields['description_label'] = ttk.Label(self, text='Description:')
        self.fields['description'] = ttk.Entry(
            self, textvariable=self.description)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="", wraplength=370)
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        create_button = ttk.Button(
            self, text='Create Menu Item ', command=self.add_record)
        create_button.pack(anchor=tk.E, padx=5, pady=5)

    def add_record(self):
        for name in menu_data:
            if name == self.item_name.get():
                self.fields['message']["text"] = "An item with this name already exists."
                return
        branch_id = State.branch_id
        if branch_id is None:
            self.fields['message']["text"] = "Current user isn't logged into or assigned a branch, Choose a branch on login first to create branch items"
            return
        self.fields['message']["text"] = ""
        item_data = {"name": self.item_name.get(
        ), "price": self.price.get(), "desc": self.description.get()}
        branch_id = State.branch_id
        create = API.post(
            f"{URL}/branches/{branch_id}/menu/create", json=item_data)
        print(create.json())
        match create.status_code:
            case 200:
                self.fields['message']["text"] = "Inventory Item Created Successfully"

                # item_id = menu_data[self.item_name.get()]
                # create_category = API.post(
                #     f"{URL}/branches/{branch_id}/menu/categories/create", json={"name": self.category.get()})
                # set_category = API.post(
                #     f"{URL}/branches/{branch_id}/menu/{item_id}/set/category", json={"name": self.category.get()})
                # print(create_category.json())
            case 400 | 409 | 401:
                self.fields['message']["text"] = create.json()["message"]


class UpdateItem(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.item_name = tk.StringVar()
        self.category = tk.StringVar()
        self.new_price = tk.DoubleVar()
        self.new_description = tk.StringVar()

        self.fields = {}

        self.fields['item_name_label'] = ttk.Label(
            self, text='Find Item By Name:')
        self.fields['item_name'] = ttk.Entry(self, textvariable=self.item_name)
        self.fields['category_label'] = ttk.Label(
            self, text='Set Item Category:')
        self.fields['category'] = ttk.Entry(self, textvariable=self.category)
        self.fields['new_price_label'] = ttk.Label(
            self, text='Enter New Price:')
        self.fields['new_price'] = ttk.Entry(self, textvariable=self.new_price)
        self.fields['new_description_label'] = ttk.Label(
            self, text='Enter New Description:')
        self.fields['new_description'] = ttk.Entry(
            self, textvariable=self.new_description)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        update_button = ttk.Button(
            self, text='Update Inventory Item ', command=self.update_record)
        update_button.pack(anchor=tk.E, padx=5, pady=5)
        delete_button = ttk.Button(
            self, text='Delete Inventory Item ', command=self.delete_record)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def update_record(self):
        branch_id = State.branch_id
        if branch_id is None:
            self.fields['message']["text"] = "Current user isn't logged into or assigned a branch, Choose a branch on login first to update branch items"
            return
        is_found = False
        for name in menu_data:
            if name == self.item_name.get():
                is_found = True
                break
        if is_found == False:
            self.fields['message']["text"] = "This menu item does not exist."
            return
        item = self.item_name.get()
        price = self.new_price.get()
        description = self.new_description.get()
        category = self.category.get()
        item_id = menu_data[item]
        if item != "":
            set_price = API.post(
                f"{URL}/branches/{branch_id}/menu/{item_id}/set/price", json={"price": price})
            match set_price.status_code:
                case 200:
                    self.fields['message']["text"] = "Information updated successfully"
                case 400 | 409 | 401:
                    self.fields['message']["text"] = set_price.json()[
                        "message"]
                    return
            if description != "":
                set_description = API.post(
                    f"{URL}/branches/{branch_id}/menu/{item_id}/set/description", json={"description": description})
                match set_description.status_code:
                    case 200:
                        self.fields['message']["text"] = "Information updated successfully"
                    case 400 | 409 | 401:
                        self.fields['message']["text"] = set_description.json()[
                            "message"]
                        return
            if category != "":
                create_category = API.post(
                    f"{URL}/branches/{branch_id}/menu/categories/create", json={"name": self.category.get()})
                print(create_category.json())
                category_id = create_category.json()["data"]["id"]
                set_category = API.post(
                    f"{URL}/branches/{branch_id}/menu/{item_id}/set/category", json={"category_id": category_id})
                print(set_category.json())
                match set_category.status_code:
                    case 200:
                        self.fields['message']["text"] = "Information updated successfully"
                    case 400 | 409 | 401:
                        self.fields['message']["text"] = set_category.json()[
                            "message"]
                        return
        else:
            self.fields['message']["text"] = "Please enter an item name."

    def delete_record(self):
        item = self.item_name.get()
        item_id = menu_data[item]
        branch_id = State.branch_id
        for record in menu_data:
            if self.item_name.get() == record:
                delete_item = API.post(
                    f"{URL}/branches/{branch_id}/menu/{item_id}/delete")
                break
        match delete_item.status_code:
            case 200:
                self.fields['message']["text"] = "Menu Item Deleted Successfully"
