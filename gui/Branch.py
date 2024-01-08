from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State


class BranchesPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = ViewBranches(notebook)
        self.frame2 = CreateBranch(notebook)
        self.frame3 = UpdateBranch(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='View All Branches')
        notebook.add(self.frame2, text='Create Branch')
        notebook.add(self.frame3, text='Update Branch')

    def on_tab_selected(self, event):
        # ref: https://www.homeandlearn.uk/python-database-form-tabs3.html
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Branches":
            self.frame1.load_records()
        if tab_text == "Create Branch":
            self.frame2.fields['message']['text'] = ""
            self.frame2.create_dropdown()
        if tab_text == "Update Branch":
            self.frame1.load_records()
            self.frame3.create_dropdown()
            self.frame3.fields['message']['text'] = ""


class ViewBranches(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('branch_name', 'address', 'city_name')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('branch_name', text='Branch')
        self.tree.heading('address', text='Address')
        self.tree.heading('city_name', text='City')
        self.load_records()
        delete_button = ttk.Button(
            self, text='Delete All Records', command=self.delete_all_records)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        all_branches = API.post(f"{URL}/branches").json()

        global branch_data
        branch_data = {}
        for branch in all_branches["data"]["branches"]:
            address = API.post(
                f"{URL}/branches/{branch["id"]}").json()["data"]["address"]
            self.tree.insert('', 'end', values=(
                branch["name"], address, branch["city"]["name"]))
            branch_data[branch["name"]] = branch["id"]

        self.tree.pack(fill='x', expand=True)

    def delete_all_records(self):
        branches_ids = []
        for record in branch_data:
            branches_ids.append(branch_data[f"{record}"])
        for id in branches_ids:
            API.post(f"{URL}/branches/{id}/delete", json=id)
        self.load_records()


class CreateBranch(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.branch_name = tk.StringVar()
        self.address = tk.StringVar()
        self.city_name_var = tk.StringVar()
        self.city_name_var.set("Choose City")

        self.fields = {}
        self.fields['branch_name_label'] = ttk.Label(self, text='Branch Name:')
        self.fields['branch_name'] = ttk.Entry(
            self, textvariable=self.branch_name)
        self.fields['address_label'] = ttk.Label(self, text='Address:')
        self.fields['address'] = ttk.Entry(self, textvariable=self.address)
        self.fields['city_name_label'] = ttk.Label(self, text='City Name:')
        self.message = ttk.Label(self, text="")

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.drop = None
        self.create_dropdown()

    def create_dropdown(self):

        dropdown = []

        global city_data
        city_data = {}
        all_cities = API.post(f"{URL}/cities").json()
        for city in all_cities["data"]["cities"]:
            dropdown.append(city["name"])
            city_data[city["name"]] = city["id"]

        if len(dropdown) == 0:
            if self.drop is not None:
                self.drop.pack_forget()
                self.create_button.pack_forget()
                self.drop = None

            self.message.pack(anchor=tk.NW, padx=10, pady=5,
                              fill=tk.X, expand=True)
            self.message.config(
                text="Please create a city first to update or create branches")
            return

        if self.drop is not None:
            return

        self.message.config(text="")
        self.drop = OptionMenu(self, self.city_name_var, *dropdown)
        self.drop.pack(anchor=tk.W, padx=10, pady=5)

        self.create_button = ttk.Button(
            self, text='Create Branch ', command=self.add_record)
        self.create_button.pack(anchor=tk.W, padx=10,
                                pady=5, fill=tk.X, expand=True)

    def add_record(self):
        branch = self.branch_name.get()
        address = self.address.get()
        city = self.city_name_var.get()
        if city != "Choose City":
            city_id = city_data[city]
        else:
            self.fields['message']["text"] = "Please choose a city."
            return
        create_data = {"name": branch, "address": address, "city_id": city_id}
        create = API.post(f"{URL}/branches/create", json=create_data)
        match create.status_code:
            case 200:
                self.fields['message']["text"] = "Branch Created Successfully"
                self.city_name_var.set("")
            case 400 | 409 | 401:
                self.fields['message']["text"] = create.json()["message"]


class UpdateBranch(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.branch_name = tk.StringVar()
        self.address = tk.StringVar()
        self.city_name_var = tk.StringVar()
        self.city_name_var.set("Choose City")

        self.fields = {}
        self.fields['branch_name_label'] = ttk.Label(self, text='Branch Name:')
        self.fields['branch_name'] = ttk.Entry(
            self, textvariable=self.branch_name)
        self.fields['address_label'] = ttk.Label(self, text='Address:')
        self.fields['address'] = ttk.Entry(self, textvariable=self.address)
        self.fields['city_name_label'] = ttk.Label(self, text='City Name:')
        self.message = ttk.Label(self, text="")

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.drop = None
        self.create_dropdown()

        delete_button = ttk.Button(
            self, text='Delete Branch', command=self.delete_record)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def create_dropdown(self):

        dropdown = []

        global city_data
        city_data = {}
        all_cities = API.post(f"{URL}/cities").json()
        for city in all_cities["data"]["cities"]:
            dropdown.append(city["name"])
            city_data[city["name"]] = city["id"]

        if len(dropdown) == 0:
            if self.drop is not None:
                self.drop.pack_forget()
                self.update_button.pack_forget()
                self.drop = None

            self.message.pack(anchor=tk.NW, padx=10, pady=5,
                              fill=tk.X, expand=True)
            self.message.config(
                text="Please create a city first to update or create branches")
            return

        if self.drop is not None:
            return

        self.message.config(text="")
        self.drop = OptionMenu(self, self.city_name_var, *dropdown)
        self.drop.pack(anchor=tk.W, padx=10, pady=5)

        self.update_button = ttk.Button(
            self, text='Update Branch', command=self.update_record)
        self.update_button.pack(anchor=tk.E, padx=5, pady=5)

    def update_record(self):
        branch = self.branch_name.get()
        if branch != "":
            is_found = False
            for branch_name in branch_data:
                if branch_name == branch:
                    is_found = True
                    break
            if is_found == False:
                self.fields['message']["text"] = "This branch does not exist."
                return
            branch_id = branch_data[branch]
            address = self.address.get()
            city = self.city_name_var.get()

            if address != "":
                set_address = API.post(
                    f"{URL}/branches/{branch_id}/set/address", json={"address": address})
                match set_address.status_code:
                    case 200:
                        self.fields['message']["text"] = "Branch Updated Successfully"
                    case 400 | 409 | 401:
                        self.fields['message']["text"] = set_address.json()[
                            "message"]
                        return
            if city != "Choose City":
                city_id = city_data[city]
                set_city = API.post(
                    f"{URL}/branches/{branch_id}/set/city", json={"city_id": city_id})
                match set_city.status_code:
                    case 200:
                        self.fields['message']["text"] = "Branch Updated Successfully"
                    case 400 | 409 | 401:
                        self.fields['message']["text"] = set_city.json()[
                            "message"]
                        return
        else:
            self.fields['message']["text"] = "Please enter a branch name to find the branch to update"

    def delete_record(self):
        branch = (self.branch_name.get())
        branch_id = branch_data[branch]
        delete_branch = API.post(
            f"{URL}/branches/{branch_id}/delete", json=branch_id)
        match delete_branch.status_code:
            case 200:
                self.fields['message']["text"] = "Branch Deleted Successfully"
