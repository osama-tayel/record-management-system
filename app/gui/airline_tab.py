"""GUI tab for managing airline records.

Placeholder layout with Treeview and form scaffolding.
Full CRUD wiring to be completed in S1-09.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict

from app.models.airline import get_airlines


# Treeview columns (key, heading, width)
AIRLINE_COLUMNS = [
    ("ID", "ID", 80),
    ("Company Name", "Company Name", 300),
]


class AirlineTab:
    """Airline record management tab (layout scaffold)."""

    def __init__(self, parent: ttk.Frame, records: List[Dict]) -> None:
        """Initialise the airline tab inside the given parent frame."""

        self.parent = parent
        self.records = records
        self.field_vars: Dict[str, tk.StringVar] = {}

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        self._build_form(parent)
        self._build_table(parent)
        self.refresh_table()

    def _build_form(self, parent: ttk.Frame) -> None:
        """Build the airline input form."""

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
        """Build the Treeview table for airline records."""

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
        """Reload the table with all airline records."""

        self.tree.delete(*self.tree.get_children())
        col_keys = [c[0] for c in AIRLINE_COLUMNS]
        for record in get_airlines(self.records):
            self.tree.insert(
                "", "end", values=[record.get(k, "") for k in col_keys]
            )
