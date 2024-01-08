# Author: Dina Hassanein (22066792)
from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State


class TablesPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = TableHomePage(notebook)
        self.frame2 = ViewTables(notebook)
        self.frame3 = CreateTable(notebook)
        self.frame4 = UpdateTable(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='Home')
        notebook.add(self.frame2, text='View All Tables')
        notebook.add(self.frame3, text='Create Table')
        notebook.add(self.frame4, text='Update Table')

    def on_tab_selected(self, event):
        # ref: https://www.homeandlearn.uk/python-database-form-tabs3.html
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Tables":
            self.frame2.load_records()
        if tab_text == "Create Table":
            self.frame3.fields['message']['text'] = ""
            self.frame2.load_records()
        if tab_text == "Update Table":
            self.frame2.load_records()
            self.frame4.fields['message']['text'] = ""


class ViewTables(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('table_number', 'capacity')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('table_number', text='Table Number')
        self.tree.heading('capacity', text='Capacity')

        delete_button = ttk.Button(
            self, text='Delete All Records', command=self.delete_all_records)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def load_records(self):
        if State.branch_id is None:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        branch_id = State.branch_id
        branch_tables_res = API.post(
            f"{URL}/branches/{branch_id}/tables")
        branch_tables = branch_tables_res.json()

        global table_data
        table_data = []

        for table in branch_tables["data"]["tables"]:
            self.tree.insert('', 'end', values=(
                table["number"], table["capacity"]))
            table_data.append(table["number"])

        self.tree.pack(fill='x', expand=True)

    def delete_all_records(self):
        branch_id = State.branch_id
        for table_number in table_data:
            res = API.post(
                f"{URL}/branches/{branch_id}/tables/{table_number}/delete")
        self.load_records()


class TableHomePage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ttk.Label(self, text="Table management page")
        label.pack()


class CreateTable(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.table_number = tk.IntVar()
        self.capacity = tk.IntVar()

        self.fields = {}

        self.fields['table_number_label'] = ttk.Label(
            self, text='Table Number:')
        self.fields['table_number'] = ttk.Entry(
            self, textvariable=self.table_number)
        self.fields['capacity_label'] = ttk.Label(self, text='Capacity:')
        self.fields['capacity'] = ttk.Entry(self, textvariable=self.capacity)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        create_button = ttk.Button(
            self, text='Create Table', command=self.add_record)
        create_button.pack(anchor=tk.E, padx=5, pady=5)

    def add_record(self):
        branch_id = State.branch_id
        if branch_id is None:
            self.fields['message']["text"] = "Current user isn't logged into or assigned a branch, Choose a branch on login first to create branch items"
            return
        number = self.table_number.get()
        capacity = self.capacity.get()
        for table_number in table_data:
            if table_number == number:
                self.fields['message']["text"] = "A table with this number already exists."
                return
        if number != "":
            if number != 0:
                if capacity != 0:
                    table_info = {"table_number": number, "capacity": capacity}
                    create = API.post(
                        f"{URL}/branches/{branch_id}/tables/create", json=table_info)
                    match create.status_code:
                        case 200:
                            self.fields['message']["text"] = "Branch Table Created Successfully"
                        case 400 | 409 | 401:
                            self.fields['message']["text"] = create.json()[
                                "message"]
                else:
                    self.fields['message']["text"] = "Table capacity cannot be 0."
                    return
            else:
                self.fields['message']["text"] = "Table number cannot be 0."
                return
        else:
            self.fields['message']["text"] = "Please enter a table number."
            return


class UpdateTable(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.table_number = tk.IntVar()

        self.fields = {}
        self.fields['tab_title'] = ttk.Label(
            self, text="Update Table Information")
        self.fields['find_table'] = ttk.Label(
            self, text='Find Table by Table Number:')
        self.fields['table_number'] = ttk.Entry(
            self, textvariable=self.table_number)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)
        delete_button = ttk.Button(
            self, text='Delete Table', command=self.delete_record)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def delete_record(self):
        number = self.table_number.get()
        branch_id = State.branch_id
        found = False
        for table_number in table_data:
            if table_number == number:
                found = True
                delete_item = API.post(
                    f"{URL}/branches/{branch_id}/tables/{number}/delete")
                break
        if found == False:
            self.fields['message']["text"] = "No table exists with this number"
            return
        match delete_item.status_code:
            case 200:
                self.fields['message']["text"] = "Branch Table Deleted Successfully"
