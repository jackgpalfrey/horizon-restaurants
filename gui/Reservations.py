from gui_lib import Page
import tkinter as tk
from tkinter import *
from tkinter import ttk
from api import API, URL, State
from datetime import datetime


class ReservationsPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.notebook = self.create_notebook_widget()

    def create_notebook_widget(self):

        style = ttk.Style(self)
        style.configure('lefttab.TNotebook', tabposition='wn')

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # create frames
        self.frame1 = ReservationsHomePage(notebook)
        self.frame2 = ViewReservations(notebook)
        self.frame3 = CreateReservation(notebook)

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        notebook.add(self.frame1, text='Home')
        notebook.add(self.frame2, text='View All Reservations')
        notebook.add(self.frame3, text='Create Reservation')

    def on_tab_selected(self, event):
        # ref: https://www.homeandlearn.uk/python-database-form-tabs3.html
        if State.username is None:
            return
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View All Reservations":
            self.frame2.load_records()
        if tab_text == "Create Reservation":
            self.frame2.load_records()


class ViewReservations(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        columns = ('customer_name', 'num_people', 'time', 'table_number')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('customer_name', text='Customer Name')
        self.tree.heading('num_people', text='Number of Guests')
        self.tree.heading('time', text='Time of Reservation')
        self.tree.heading('table_number', text='Table Number')

    def load_records(self):
        if State.branch_id is None:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        branch_id = State.branch_id
        branch_reservations_res = API.post(
            f"{URL}/branches/{branch_id}/reservations")
        branch_reservation = branch_reservations_res.json()
        print(branch_reservation, "!!!!")

        global res_data
        res_data = {}

        for res_info in branch_reservation["data"]["reservations"]:
            self.tree.insert('', 'end', values=(
                res_info["customer"], res_info["num_people"], res_info["time"], res_info["table_num"]))
            res_data[res_info["customer"]] = res_info["id"]
            # customer_name = res_info["name"]
            # item_id = res_info["id"]
            # table_id = res_info["table"]["id"]
            # res_data[customer_name] = (item_id, table_id)

        self.tree.pack(fill='x', expand=True)


class ReservationsHomePage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ttk.Label(self, text="Menu Management Page")
        label.pack()


class CreateReservation(ttk.Frame):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.customer_name = tk.StringVar()
        self.num_people = tk.IntVar()
        self.time = tk.StringVar()
        self.table_no = tk.IntVar()

        self.fields = {}

        self.fields['customer_name_label'] = ttk.Label(
            self, text='Customer Name:')
        self.fields['customer_name'] = ttk.Entry(
            self, textvariable=self.customer_name)
        self.fields['num_people_label'] = ttk.Label(
            self, text='Number of Guests:')
        self.fields['num_people'] = ttk.Entry(
            self, textvariable=self.num_people)
        self.fields['time_label'] = ttk.Label(
            self, text='Time of Reservation: (Please note reservation time must be in the format DD-MM-YYYY HH:MM:SS)')
        self.fields['time'] = ttk.Entry(self, textvariable=self.time)
        self.message = ttk.Label(self, text="")
        self.fields['table_num_label'] = ttk.Label(self, text='Table Number:')
        self.fields['table_num'] = ttk.Entry(self, textvariable=self.table_no)

        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.fields['message'] = ttk.Label(self, text="", wraplength=370)
        self.fields['message'].pack(
            anchor=tk.W, padx=10, pady=5, fill=tk.X, expand=True)

        self.create_button = ttk.Button(
            self, text='Create Reservation ', command=self.add_record)
        self.create_button.pack(anchor=tk.E, padx=5, pady=5)

    def add_record(self):
        branch_id = State.branch_id
        if branch_id is None:
            self.fields['message']["text"] = "Current user isn't logged into or assigned a branch, Choose a branch on login first to create branch items"
            return
        self.fields['message']["text"] = ""
        res_time = datetime.strptime(self.time.get(), '%d-%m-%Y %H:%M:%S')
        unix_timestamp = res_time.timestamp()
        res_info = {"customer_name": self.customer_name.get(
        ), "num_people": self.num_people.get(), "reservation_timestamp": unix_timestamp, "table_number": self.table_no.get()}
        branch_id = State.branch_id
        create = API.post(
            f"{URL}/branches/{branch_id}/reservations/create", json=res_info)
        print(create.json(), "Just in case")
        match create.status_code:
            case 200:
                self.fields['message']["text"] = "Reservation Created Successfully"
            case 400 | 409 | 401:
                self.fields['message']["text"] = create.json()["message"]
