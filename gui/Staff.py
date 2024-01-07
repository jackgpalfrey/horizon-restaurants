from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State


class StaffPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = StaffHomePage(notebook)
        self.frame2 = ViewStaff(notebook)
        self.frame3 = CreateUser(notebook)
        self.frame4 = UpdateUser(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='Home')
        notebook.add(self.frame2, text='View All Branch Staff')
        notebook.add(self.frame3, text='Create Staff Member')
        notebook.add(self.frame4, text='Update Staff Member')

    def on_tab_selected(self, event):
        # ref: https://www.homeandlearn.uk/python-database-form-tabs3.html
        if State.username is None:
            return
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Branch Staff":
            self.frame2.load_records()


class ViewStaff(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('full_name', 'username', 'role', 'branch')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('full_name', text='Full Name')
        self.tree.heading('username', text='Username')
        self.tree.heading('role', text='Role')
        self.tree.heading('branch', text='Branch')

        delete_button = ttk.Button(
            self, text='Delete All Records', command=self.delete_all_records)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def load_records(self):
        if State.branch_id is None:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        branch_id = State.branch_id
        branch_users_res = API.post(f"{URL}/branches/{branch_id}/users")
        branch_users = branch_users_res.json()

        global user_data
        user_data = []

        for user in branch_users["data"]["users"]:
            self.tree.insert('', 'end', values=(
                user["full_name"], user["username"], user["role"]["name"], user["branch"]["name"]))
            user_data.append(user["username"])

        self.tree.pack(fill='x', expand=True)

    def delete_all_records(self):
        for record in user_data:
            res = API.post(f"{URL}/users/{record}/delete")
        self.load_records()


class StaffHomePage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ttk.Label(self, text="Staff management page")
        label.pack()


class CreateUser(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.username = tk.StringVar()
        self.full_name = tk.StringVar()
        self.password = tk.StringVar()
        self.role = tk.StringVar()

        self.fields = {}

        self.fields['fullname_label'] = ttk.Label(self, text='Full Name:')
        self.fields['fullname'] = ttk.Entry(self, textvariable=self.full_name)
        self.fields['username_label'] = ttk.Label(self, text='Username:')
        self.fields['username'] = ttk.Entry(self, textvariable=self.username)
        self.fields['password_label'] = ttk.Label(self, text='Password:')
        self.fields['password'] = ttk.Entry(self, textvariable=self.password)
        self.fields['role_label'] = ttk.Label(self, text='Select Role:')

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        global selected_role, selected_branch
        selected_role = StringVar()
        options = [
            "0. Staff",
            "1. Frontend Staff",
            "2. Kitchen Staff",
            "3. Chef",
            "4. Manager",
            "99. Admin"
        ]
        selected_role.set("0. Staff")
        drop = OptionMenu(self, selected_role, *options)
        drop.pack(anchor=tk.W, padx=10, pady=5)

        selected_branch = StringVar()
        self.all_branches_res = API.post(f"{URL}/branches")
        self.all_branches = self.all_branches_res.json()

        dropdown = []
        global branch_data
        branch_data = {}
        for branch in self.all_branches["data"]["branches"]:
            dropdown.append(branch["name"])
            branch_data[branch["name"]] = branch["id"]

        display_text = dropdown[0]
        selected_branch.set(display_text)
        drop = OptionMenu(self, selected_branch, *dropdown)
        drop.pack(anchor=tk.N, padx=0, pady=0)

        self.fields['message'] = ttk.Label(self, text="", wraplength=370)
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        create_button = ttk.Button(
            self, text='Create Staff Member ', command=self.add_record)
        create_button.pack(anchor=tk.E, padx=5, pady=5)

    def add_record(self):
        role_id = int(selected_role.get().split(".")[0])
        user_data = {"username": self.username.get(), "full_name": self.full_name.get(
        ), "password": self.password.get(), "role_id": role_id}
        create = API.post(f"{URL}/users/create", json=user_data)
        match create.status_code:
            case 200:
                self.fields['message']["text"] = "User Created Successfully"
                branch_name = selected_branch.get()
                branch_id = branch_data[branch_name]
                branch = API.post(
                    f"{URL}/branches/{branch_id}/users/add", json={"username": self.username.get()})
            case 400 | 409 | 401:
                self.fields['message']["text"] = create.json()["message"]


class UpdateUser(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.username = tk.StringVar()
        self.full_name = tk.StringVar()
        self.new_full_name = tk.StringVar()
        self.password = tk.StringVar()
        self.new_password = tk.StringVar()
        self.role = tk.StringVar()
        self.new_role = tk.StringVar()

        self.fields = {}
        self.fields['tab_title'] = ttk.Label(
            self, text="Update Staff Information")
        self.fields['find_user'] = ttk.Label(
            self, text='Find Staff Member by Username:')
        self.fields['username'] = ttk.Entry(self, textvariable=self.username)
        self.fields['new_full_name_label'] = ttk.Label(
            self, text='Enter New Full Name:')
        self.fields['new_full_name'] = ttk.Entry(
            self, textvariable=self.new_full_name)
        self.fields['new_password_label'] = ttk.Label(
            self, text='Enter New Password:')
        self.fields['new_password'] = ttk.Entry(
            self, textvariable=self.new_password)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['new_role_label'] = ttk.Label(
            self, text='Select New Role:')
        self.fields['new_role_label'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        global new_role_selection
        new_role_selection = StringVar()

        options = [
            "0. Staff",
            "1. Frontend Staff",
            "2. Kitchen Staff",
            "3. Chef",
            "4. Manager",
            "99. Admin"
        ]
        new_role_selection.set("0. Staff")
        drop = OptionMenu(self, new_role_selection, *options)
        drop.pack(anchor=tk.W, padx=10, pady=5)

        self.fields['message'] = ttk.Label(self, text="")
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        update_button = ttk.Button(
            self, text='Update Staff Member ', command=self.update_record)
        update_button.pack(anchor=tk.E, padx=5, pady=5)
        delete_button = ttk.Button(
            self, text='Delete Staff Member ', command=self.delete_record)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def update_record(self):
        username = self.username.get()
        full_name = self.new_full_name.get()
        password = self.new_password.get()
        if new_role_selection is not None:
            role_id = int(new_role_selection.get().split(".")[0])
        if full_name != "":
            set_name = API.post(
                f"{URL}/users/{username}/set/fullname", json={"full_name": full_name})
        if password != "":
            set_password = API.post(
                f"{URL}/users/{username}/set/password", json={"password": password})
        if role_id != "":
            set_role = API.post(
                f"{URL}/users/{username}/set/role", json={"role_id": role_id})
        if full_name != "":
            match set_name.status_code:
                case 200:
                    self.fields['message']["text"] = "Information updated successfully"
                case 400 | 409 | 401:
                    self.fields['message']["text"] = set_name.json()["message"]
                    return
        if password != "":
            match set_password.status_code:
                case 200:
                    self.fields['message']["text"] = "Information updated successfully"
                case 400 | 409 | 401:
                    self.fields['message']["text"] = "Invalid Password"
                    return
        if role_id != "":
            match set_role.status_code:
                case 200:
                    self.fields['message']["text"] = "Information updated successfully"
                case 400 | 409 | 401:
                    self.fields['message']["text"] = set_role.json()["message"]
                    return

    def delete_record(self):
        for record in user_data:
            if self.username.get() == record:
                delete_user = API.post(
                    f"{URL}/users/{self.username.get()}/delete", json=self.username.get())
                break
        match delete_user.status_code:
            case 200:
                self.fields['message']["text"] = "Staff Member Deleted Successfully"
