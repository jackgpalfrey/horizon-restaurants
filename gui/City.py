from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State


class CitiesPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = ViewCities(notebook)
        self.frame2 = CreateCity(notebook)
        self.frame3 = UpdateCity(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='View All Cities')
        notebook.add(self.frame2, text='Create City')
        notebook.add(self.frame3, text='Update City')

    def on_tab_selected(self, event):
        # ref:
        # https://www.homeandlearn.uk/python-database-form-tabs3.html#:~:text=
        # You%20do%20the%20binding%20on,that%20you%20want%20to%20implement.&text=Between%
        # 20double%20quotes%20and%20double,deal%20with%20this%20event%3A%20on_tab_selected
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Cities":
            self.frame1.load_records()
        if tab_text == "Create City":
            self.frame2.fields['message']['text'] = ""
        if tab_text == "Update City":
            self.frame1.load_records()
            self.frame3.fields['message']['text'] = ""


class ViewCities(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('city_name')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('city_name', text='Cities')
        self.load_records()
        delete_button = ttk.Button(
            self, text='Delete All Records', command=self.delete_all_records)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        all_cities_res = API.post(f"{URL}/cities")
        all_cities = all_cities_res.json()
        global city_data
        city_data = {}
        for city in all_cities["data"]["cities"]:
            self.tree.insert('', 'end', values=(f"{city["name"]}"))
            data = {city["name"]: city["id"]}
            city_data.update(data)

        self.tree.pack(fill='x', expand=True)

    def delete_all_records(self):
        cities_ids = []
        for record in city_data:
            cities_ids.append(city_data[f"{record}"])
        for id in cities_ids:
            API.post(f"{URL}/cities/{id}/delete", json=id)
        self.load_records()


class CreateCity(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.city_name = tk.StringVar()

        self.fields = {}
        self.fields['city_name_label'] = ttk.Label(self, text='City Name:')
        self.fields['city_name'] = ttk.Entry(self, textvariable=self.city_name)
        self.fields['message'] = ttk.Label(self, text="")

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        create_button = ttk.Button(
            self, text='Create City ', command=self.add_record)
        create_button.pack(anchor=tk.E, padx=5, pady=5)

    def add_record(self):
        city = (self.city_name.get())
        city_data = {"name": city}
        create = API.post(f"{URL}/cities/create", json=city_data)
        match create.status_code:
            case 200:
                self.fields['message']["text"] = "City Created Successfully"
                self.city_name.set("")
            case 400:
                self.fields['message']["text"] = "Invalid City Name"


class UpdateCity(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.city_name = tk.StringVar()
        self.new_name = tk.StringVar()

        self.fields = {}
        self.fields['tab_title'] = ttk.Label(
            self, text="Update City Information")
        self.fields['find_city'] = ttk.Label(self, text='Find City:')
        self.fields['city_name'] = ttk.Entry(self, textvariable=self.city_name)
        self.fields['new_name_label'] = ttk.Label(
            self, text='Enter New City Name:')
        self.fields['new_city_name'] = ttk.Entry(
            self, textvariable=self.new_name)
        self.fields['message'] = ttk.Label(self, text="")

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        update_button = ttk.Button(
            self, text='Update City ', command=self.update_record)
        update_button.pack(anchor=tk.E, padx=5, pady=5)
        delete_button = ttk.Button(
            self, text='Delete City ', command=self.delete_record)
        delete_button.pack(anchor=tk.E, padx=5, pady=5)

    def update_record(self):
        city = (self.city_name.get())
        city_id = city_data[city]
        name_data = self.new_name.get()
        set_name = API.post(
            f"{URL}/cities/{city_id}/set/name", json={"name": name_data})
        match set_name.status_code:
            case 200:
                self.fields['message']["text"] = "City Name Set Successfully"
            case 400:
                self.fields['message']["text"] = "Invalid City Name"
            case 409:
                self.fields['message']["text"] = "City Already Exists"

    def delete_record(self):
        city = (self.city_name.get())
        city_id = city_data[city]
        delete_city = API.post(
            f"{URL}/cities/{city_id}/delete", json=city_id)
        match delete_city.status_code:
            case 200:
                self.fields['message']["text"] = "City Deleted Successfully"
