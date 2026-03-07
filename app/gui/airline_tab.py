  feature/airline-crud
"""
Airline Tab GUI

Provides the graphical interface for managing airline records.
Connects the airline model CRUD functions with the Tkinter GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from app.models.airline import (
    create_airline,
    validate_airline,
    get_airlines,
    update_airline,
    delete_airline,
    search_airlines,
)


class AirlineTab:
    """GUI tab responsible for airline record management."""

    def __init__(self, parent):

        self.parent = parent

        # Local record storage (shared storage will be implemented later)
        self.records = []

        # =========================
        # Tkinter Variables
        # =========================

        self.company_name_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # =========================
        # Airline Form
        # =========================

        form_frame = ttk.LabelFrame(parent, text="Airline Information")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Company Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        ttk.Entry(
            form_frame,
            textvariable=self.company_name_var,
            width=40,
        ).grid(row=0, column=1, padx=5, pady=5)

        # =========================
        # CRUD Buttons
        # =========================

        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Save", command=self.save_record).pack(
            side="left", padx=5
        )

        ttk.Button(button_frame, text="Update", command=self.update_record).pack(
            side="left", padx=5
        )

        ttk.Button(button_frame, text="Delete", command=self.delete_record).pack(
            side="left", padx=5
        )

        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(
            side="left", padx=5
        )

        # =========================
        # Search Section
        # =========================

        search_frame = ttk.LabelFrame(parent, text="Search Airlines")
        search_frame.pack(fill="x", padx=10, pady=10)

        ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40,
        ).pack(side="left", padx=5, pady=5)

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_records,
        ).pack(side="left", padx=5)

        # =========================
        # Treeview Table
        # =========================

        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Company Name"),
            show="headings",
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Company Name", text="Company Name")

        self.tree.column("ID", width=80)
        self.tree.column("Company Name", width=300)

        self.tree.pack(fill="both", expand=True)

        # When user clicks a row
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # =====================================
    # Helper Method
    # =====================================

    def next_id(self):
        """Generate the next airline ID."""

        airlines = get_airlines(self.records)

        if not airlines:
            return 1

        return max(a["ID"] for a in airlines) + 1

    # =====================================
    # CRUD Methods
    # =====================================

    def save_record(self):
        """Create a new airline record."""

        company_name = self.company_name_var.get().strip()

        valid, error = validate_airline(company_name)

        if not valid:
            messagebox.showerror("Validation Error", error)
            return

        airline_id = self.next_id()

        airline = create_airline(airline_id, company_name)

        # Prevent accidental duplicate object insertion
        if airline not in self.records:
            self.records.append(airline)

        self.refresh_treeview()
        self.clear_form()

        messagebox.showinfo("Success", "Airline record created.")

    def update_record(self):
        """Update the selected airline record."""

        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "Select a record to update.")
            return

        item = self.tree.item(selected[0])
        airline_id = item["values"][0]

        company_name = self.company_name_var.get().strip()

        valid, error = validate_airline(company_name)

        if not valid:
            messagebox.showerror("Validation Error", error)
            return

        update_airline(
            self.records,
            airline_id,
            {"Company Name": company_name},
        )

        self.refresh_treeview()

        messagebox.showinfo("Success", "Airline record updated.")

    def delete_record(self):
        """Delete the selected airline record."""

        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "Select a record to delete.")
            return

        confirm = messagebox.askokcancel(
            "Delete",
            "Are you sure you want to delete this airline?",
        )

        if not confirm:
            return

        item = self.tree.item(selected[0])
        airline_id = item["values"][0]

        delete_airline(self.records, airline_id)

        self.refresh_treeview()
        self.clear_form()

    def clear_form(self):
        """Clear form inputs."""

        self.company_name_var.set("")

    def search_records(self):
        """Search airline records."""

        search_term = self.search_var.get()

        results = search_airlines(self.records, search_term)

        self.tree.delete(*self.tree.get_children())

        for record in results:
            self.tree.insert(
                "",
                "end",
                values=(record["ID"], record["Company Name"]),
            )

    def refresh_treeview(self):
        """Refresh the table with all airline records."""

        self.tree.delete(*self.tree.get_children())

        for record in get_airlines(self.records):
            self.tree.insert(
                "",
                "end",
                values=(record["ID"], record["Company Name"]),
            )

    def on_row_select(self, event):
        """Populate form fields when a table row is selected."""

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        self.company_name_var.set(values[1])
 
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
     main
