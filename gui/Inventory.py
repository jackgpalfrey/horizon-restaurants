from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State


class InventoryPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = InventoryHomePage(notebook)
        self.frame2 = ViewItems(notebook)
        self.frame3 = CreateItem(notebook)
        self.frame4 = UpdateItem(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='Home')
        notebook.add(self.frame2, text='View All Inventory Items')
        notebook.add(self.frame3, text='Create Inventory Item')
        notebook.add(self.frame4, text='Update Inventory Item')

    def on_tab_selected(self, event):
        # ref: https://www.homeandlearn.uk/python-database-form-tabs3.html
        if State.username is None:
            return
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Inventory Items":
            self.frame2.load_records()
        if tab_text == "Home":
            self.frame2.load_records()
        if tab_text == "Create Inventory Item":
            self.frame2.load_records()
        if tab_text == "Update Inventory Item":
            self.frame2.load_records()


class ViewItems(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('item_name', 'quantity', 'threshold')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('item_name', text='Item Name')
        self.tree.heading('quantity', text='Quantity')
        self.tree.heading('threshold', text='Threshold')

        delete_button = ttk.Button(
            self, text='Delete All Records', command=self.delete_all_records)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def load_records(self):
        if State.branch_id is None:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        branch_id = State.branch_id
        branch_inventory_res = API.post(
            f"{URL}/branches/{branch_id}/inventory")
        branch_inventory = branch_inventory_res.json()

        global inventory_data
        inventory_data = {}

        for item in branch_inventory["data"]["inventory"]:
            self.tree.insert('', 'end', values=(
                item["name"], item["quantity"], item["threshold"]))
            item_name = item["name"]
            item_id = item["id"]
            inventory_data[item_name] = (item_name, item_id)

        self.tree.pack(fill='x', expand=True)

    def delete_all_records(self):
        branch_id = State.branch_id
        for item in inventory_data.values():
            item_id = item[1]
            res = API.post(
                f"{URL}/branches/{branch_id}/inventory/{item_id}/delete")
        self.load_records()


class InventoryHomePage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ttk.Label(self, text="Inventory management page")
        label.pack()


class CreateItem(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.item_name = tk.StringVar()
        self.quantity = tk.IntVar()
        self.threshold = tk.IntVar()

        self.fields = {}

        self.fields['item_name_label'] = ttk.Label(self, text='Item Name:')
        self.fields['item_name'] = ttk.Entry(self, textvariable=self.item_name)
        self.fields['quantity_label'] = ttk.Label(self, text='Quantity:')
        self.fields['quantity'] = ttk.Entry(self, textvariable=self.quantity)
        self.fields['threshold_label'] = ttk.Label(self, text='Threshold:')
        self.fields['threshold'] = ttk.Entry(self, textvariable=self.threshold)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        create_button = ttk.Button(
            self, text='Create Inventory Item', command=self.add_record)
        create_button.pack(anchor=tk.E, padx=5, pady=5)

    def add_record(self):
        branch_id = State.branch_id
        if branch_id is None:
            self.fields['message']["text"] = "Current user isn't logged into or assigned a branch, Choose a branch on login first to create branch items"
            return
        self.fields['message']["text"] = ""
        item_data = {"name": self.item_name.get(), "quantity": self.quantity.get(
        ), "threshold": self.threshold.get()}
        branch_id = State.branch_id
        create = API.post(
            f"{URL}/branches/{branch_id}/inventory/create", json=item_data)
        match create.status_code:
            case 200:
                self.fields['message']["text"] = "Inventory Item Created Successfully"
            case 400 | 409 | 401:
                self.fields['message']["text"] = create.json()["message"]


class UpdateItem(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.item_name = tk.StringVar()
        self.new_quantity = tk.IntVar()
        self.new_threshold = tk.IntVar()

        self.fields = {}
        self.fields['tab_title'] = ttk.Label(
            self, text="Update Inventory Item Information")
        self.fields['find_item'] = ttk.Label(
            self, text='Find Inventory Item:')
        self.fields['item_name'] = ttk.Entry(self, textvariable=self.item_name)
        self.fields['new_quantity_label'] = ttk.Label(
            self, text='Enter New Item Quantity:')
        self.fields['new_quantity'] = ttk.Entry(
            self, textvariable=self.new_quantity)
        self.fields['new_threshold_label'] = ttk.Label(
            self, text='Enter New Item Threshold:')
        self.fields['new_threshold'] = ttk.Entry(
            self, textvariable=self.new_threshold)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        update_button = ttk.Button(
            self, text='Update Inventory Item', command=self.update_record)
        update_button.pack(anchor=tk.E, padx=5, pady=5)
        delete_button = ttk.Button(
            self, text='Delete Inventory Item', command=self.delete_record)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def update_record(self):
        branch_id = State.branch_id
        if branch_id is None:
            self.fields['message']["text"] = "Current user isn't logged into or assigned a branch, Choose a branch on login first to update branch items"
            return
        item = self.item_name.get()
        quantity = self.new_quantity.get()
        threshold = self.new_threshold.get()
        found = False
        for item_name in inventory_data.keys():
            if item_name == item:
                found = True
                break
        if found == False:
            self.fields['message']["text"] = "This item does not exist."
            return
        if item != '':
            item_id = inventory_data.get(item, None)[1]
            if quantity != 0:
                set_quantity = API.post(
                    f"{URL}/branches/{branch_id}/inventory/{item_id}/set/quantity", json={"quantity": quantity})
                match set_quantity.status_code:
                    case 200:
                        self.fields['message']["text"] = "Item Information updated successfully"
                    case 400 | 409 | 401:
                        self.fields['message']["text"] = set_quantity.json()[
                            "message"]
                        return
            if threshold != 0:
                set_threshold = API.post(
                    f"{URL}/branches/{branch_id}/inventory/{item_id}/set/threshold", json={"threshold": threshold})
                match set_threshold.status_code:
                    case 200:
                        self.fields['message']["text"] = "Information updated successfully"
                    case 400 | 409 | 401:
                        self.fields['message']["text"] = set_threshold.json()[
                            "message"]
                        return
        else:
            self.fields['message']["text"] = "Please enter an item name."

    def delete_record(self):
        item = self.item_name.get()
        item_id = inventory_data.get(item, None)[1]
        branch_id = State.branch_id
        for item_name in inventory_data.keys():
            if item == item_name:
                delete_item = API.post(
                    f"{URL}/branches/{branch_id}/inventory/{item_id}/delete")
                break
        match delete_item.status_code:
            case 200:
                self.fields['message']["text"] = "Inventory Item Deleted Successfully"
