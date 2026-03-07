"""GUI tab for managing flight records."""

import tkinter as tk
from tkinter import ttk


class FlightTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.flights = []

        title = ttk.Label(self, text="Flight Records", font=("Arial", 16))
        title.pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Client ID").grid(row=0, column=0, padx=5, pady=5)
        self.client_id = ttk.Entry(form)
        self.client_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Airline ID").grid(row=1, column=0, padx=5, pady=5)
        self.airline_id = ttk.Entry(form)
        self.airline_id.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Date").grid(row=2, column=0, padx=5, pady=5)
        self.date = ttk.Entry(form)
        self.date.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Start City").grid(row=3, column=0, padx=5, pady=5)
        self.start_city = ttk.Entry(form)
        self.start_city.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form, text="End City").grid(row=4, column=0, padx=5, pady=5)
        self.end_city = ttk.Entry(form)
        self.end_city.grid(row=4, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Flight", command=self.add_flight).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Flight", command=self.delete_flight).pack(side="left", padx=5)

        columns = ("Client ID", "Airline ID", "Date", "Start City", "End City")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_flight(self):

        client = self.client_id.get()
        airline = self.airline_id.get()
        date = self.date.get()
        start = self.start_city.get()
        end = self.end_city.get()

        if client and airline and date and start and end:

            self.flights.append({
                "Client_ID": client,
                "Airline_ID": airline,
                "Date": date,
                "Start City": start,
                "End City": end
            })

            self.tree.insert("", "end", values=(client, airline, date, start, end))

            self.client_id.delete(0, tk.END)
            self.airline_id.delete(0, tk.END)
            self.date.delete(0, tk.END)
            self.start_city.delete(0, tk.END)
            self.end_city.delete(0, tk.END)

    def delete_flight(self):

        selected = self.tree.selection()

        if selected:
            self.tree.delete(selected)
