feature/gui-shell
# GUI tab for managing airline records.
# Layout with Treeview and form scaffolding. CRUD wiring in S1-09.

import tkinter as tk
from tkinter import ttk
from typing import List, Dict

from app.models.airline import get_airlines


# (key, heading, width)
AIRLINE_COLUMNS = [
    ("ID", "ID", 80),
    ("Company Name", "Company Name", 300),
]


class AirlineTab:
    """Airline record management tab (layout scaffold)."""

    def __init__(self, parent: ttk.Frame, records: List[Dict]) -> None:
        self.parent = parent
        self.records = records
        self.field_vars: Dict[str, tk.StringVar] = {}

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        self._build_form(parent)
        self._build_table(parent)
        self.refresh_table()

    def _build_form(self, parent: ttk.Frame) -> None:
        form = ttk.Frame(parent, style="TFrame")
        form.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        form.columnconfigure(1, weight=1)

        ttk.Label(
            form, text="Airline Details", style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ttk.Label(form, text="Company Name *", style="TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=4
        )
        var = tk.StringVar()
        self.field_vars["Company Name"] = var
        ttk.Entry(form, textvariable=var, style="TEntry").grid(
            row=1, column=1, sticky="ew", pady=4
        )

    def _build_table(self, parent: ttk.Frame) -> None:
        table_frame = ttk.Frame(parent, style="TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        col_keys = [c[0] for c in AIRLINE_COLUMNS]
        self.tree = ttk.Treeview(
            table_frame, columns=col_keys, show="headings", selectmode="browse"
        )

        for key, heading, width in AIRLINE_COLUMNS:
            self.tree.heading(key, text=heading, anchor="w")
            self.tree.column(key, width=width, anchor="w", minwidth=40)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def refresh_table(self) -> None:
        self.tree.delete(*self.tree.get_children())
        col_keys = [c[0] for c in AIRLINE_COLUMNS]
        for record in get_airlines(self.records):
            self.tree.insert(
                "", "end", values=[record.get(k, "") for k in col_keys]
            )

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
