# GUI tab for managing airline records

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict

from app.models.airline import get_airlines
from app.models.id_generator import get_next_id
from app.storage.json_storage import StorageManager


AIRLINE_COLUMNS = [
    ("ID", "ID", 80),
    ("Company Name", "Company Name", 300),
]


class AirlineTab:
    """Airline record management tab."""

    def __init__(self, parent: ttk.Frame, records: List[Dict]) -> None:

        self.parent = parent
        self.records = records
        self.storage = StorageManager()

        self.field_vars: Dict[str, tk.StringVar] = {}
        self.selected_record: Dict | None = None

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)

        self._build_form(parent)
        self._build_search(parent)
        self._build_table(parent)

        self.refresh_table()

    # -----------------------------
    # Form
    # -----------------------------

    def _build_form(self, parent: ttk.Frame) -> None:

        form = ttk.Frame(parent)
        form.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Airline Details").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )

        ttk.Label(form, text="Company Name *").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=4
        )

        var = tk.StringVar()
        self.field_vars["Company Name"] = var

        self.entry_name = ttk.Entry(form, textvariable=var)
        self.entry_name.grid(row=1, column=1, sticky="ew", pady=4)

        button_frame = ttk.Frame(form)
        button_frame.grid(row=2, column=1, sticky="e", pady=(10, 0))

        ttk.Button(
            button_frame,
            text="Add",
            command=self.add_airline
        ).grid(row=0, column=0, padx=4)

        self.update_btn = ttk.Button(
            button_frame,
            text="Update",
            command=self.update_airline,
            state="disabled"
        )
        self.update_btn.grid(row=0, column=1, padx=4)

        self.delete_btn = ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_airline,
            state="disabled"
        )
        self.delete_btn.grid(row=0, column=2, padx=4)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form
        ).grid(row=0, column=3, padx=4)

    # -----------------------------
    # Search
    # -----------------------------

    def _build_search(self, parent: ttk.Frame) -> None:

        search_frame = ttk.Frame(parent)
        search_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))

        ttk.Label(search_frame, text="Search Airline:").grid(
            row=0, column=0, padx=(0, 8)
        )

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.search_airlines)

        ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        ).grid(row=0, column=1, sticky="w")

    # -----------------------------
    # Table
    # -----------------------------

    def _build_table(self, parent: ttk.Frame) -> None:

        table_frame = ttk.Frame(parent)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        col_keys = [c[0] for c in AIRLINE_COLUMNS]

        self.tree = ttk.Treeview(
            table_frame,
            columns=col_keys,
            show="headings",
            selectmode="browse"
        )

        for key, heading, width in AIRLINE_COLUMNS:
            self.tree.heading(
                key,
                text=heading,
                command=lambda c=key: self.sort_column(c, False)
            )
            self.tree.column(key, width=width)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # -----------------------------
    # Refresh table
    # -----------------------------

    def refresh_table(self) -> None:

        self.tree.delete(*self.tree.get_children())

        col_keys = [c[0] for c in AIRLINE_COLUMNS]

        for record in get_airlines(self.records):

            self.tree.insert(
                "",
                "end",
                values=[record.get(k, "") for k in col_keys]
            )

    # -----------------------------
    # Search airlines
    # -----------------------------

    def search_airlines(self, *args) -> None:

        query = self.search_var.get().lower()

        self.tree.delete(*self.tree.get_children())

        col_keys = [c[0] for c in AIRLINE_COLUMNS]

        for record in get_airlines(self.records):

            name = record.get("Company Name", "").lower()

            if query in name:

                self.tree.insert(
                    "",
                    "end",
                    values=[record.get(k, "") for k in col_keys]
                )

    # -----------------------------
    # Sort columns
    # -----------------------------

    def sort_column(self, col, reverse):

        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        data.sort(reverse=reverse)

        for index, (val, k) in enumerate(data):
            self.tree.move(k, "", index)

        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    # -----------------------------
    # Row selection
    # -----------------------------

    def on_row_select(self, event) -> None:

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        record_id = int(values[0])

        for record in self.records:

            if record.get("ID") == record_id and record.get("Type") == "Airline":

                self.selected_record = record
                break

        if self.selected_record:

            self.field_vars["Company Name"].set(
                self.selected_record.get("Company Name", "")
            )

            self.update_btn.config(state="normal")
            self.delete_btn.config(state="normal")

    # -----------------------------
    # Add airline
    # -----------------------------

    def add_airline(self) -> None:

        name = self.field_vars["Company Name"].get().strip()

        if not name:
            messagebox.showwarning("Validation", "Company Name is required.")
            return

        for record in get_airlines(self.records):

            if record.get("Company Name", "").lower() == name.lower():

                messagebox.showerror("Duplicate", "Airline already exists.")
                return

        new_id = get_next_id(self.records, "Airline")

        airline = {
            "ID": new_id,
            "Type": "Airline",
            "Company Name": name
        }

        self.records.append(airline)

        self.storage.save(self.records)

        self.refresh_table()

        self.clear_form()

    # -----------------------------
    # Update airline
    # -----------------------------

    def update_airline(self) -> None:

        if not self.selected_record:
            messagebox.showwarning("Selection", "Select an airline first.")
            return

        name = self.field_vars["Company Name"].get().strip()

        if not name:
            messagebox.showwarning("Validation", "Company Name is required.")
            return

        record_id = self.selected_record["ID"]

        for record in self.records:

            if record.get("ID") == record_id and record.get("Type") == "Airline":

                record["Company Name"] = name
                break

        self.storage.save(self.records)

        self.refresh_table()

        self.clear_form()

    # -----------------------------
    # Delete airline
    # -----------------------------

    def delete_airline(self) -> None:

        if not self.selected_record:
            messagebox.showwarning("Selection", "Select an airline first.")
            return

        name = self.selected_record.get("Company Name", "")

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete airline '{name}'?"
        )

        if not confirm:
            return

        record_id = self.selected_record["ID"]

        for record in self.records:

            if record.get("ID") == record_id and record.get("Type") == "Airline":

                self.records.remove(record)

                break

        self.storage.save(self.records)

        self.refresh_table()

        self.clear_form()

    # -----------------------------
    # Clear form
    # -----------------------------

    def clear_form(self) -> None:

        for var in self.field_vars.values():
            var.set("")

        self.selected_record = None

        self.update_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")

        self.tree.selection_remove(self.tree.selection())

        self.entry_name.focus()
