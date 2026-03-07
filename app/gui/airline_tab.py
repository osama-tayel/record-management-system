"""GUI tab for managing airline records."""

import tkinter as tk
from tkinter import ttk


class AirlineTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.airlines = []

        title = ttk.Label(self, text="Airline Records", font=("Arial", 16))
        title.pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Airline ID").grid(row=0, column=0, padx=5, pady=5)
        self.airline_id = ttk.Entry(form)
        self.airline_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Company Name").grid(row=1, column=0, padx=5, pady=5)
        self.company_name = ttk.Entry(form)
        self.company_name.grid(row=1, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Airline", command=self.add_airline).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Airline", command=self.delete_airline).pack(side="left", padx=5)

        columns = ("ID", "Company")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_airline(self):

        airline_id = self.airline_id.get()
        company = self.company_name.get()

        if airline_id and company:

            self.airlines.append({
                "ID": airline_id,
                "Company Name": company
            })

            self.tree.insert("", "end", values=(airline_id, company))

            self.airline_id.delete(0, tk.END)
            self.company_name.delete(0, tk.END)

    def delete_airline(self):

        selected = self.tree.selection()

        if selected:
            self.tree.delete(selected)
