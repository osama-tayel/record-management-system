# GUI tab for managing flight records.
# Layout with Treeview and form scaffolding. CRUD wiring in S1-10.

import tkinter as tk
from tkinter import ttk
from typing import List, Dict

from app.models.flight import get_flights


# (key, heading, width)
FLIGHT_COLUMNS = [
    ("ID", "ID", 50),
    ("Client_ID", "Client ID", 80),
    ("Airline_ID", "Airline ID", 80),
    ("Date", "Date", 100),
    ("Start City", "From", 120),
    ("End City", "To", 120),
]


class FlightTab:
    """Flight record management tab (layout scaffold)."""

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
        form.columnconfigure(3, weight=1)

        ttk.Label(
            form, text="Flight Details", style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        fields = [
            ("Client_ID", "Client ID *"),
            ("Airline_ID", "Airline ID *"),
            ("Date", "Date (YYYY-MM-DD) *"),
            ("Start City", "From City *"),
            ("End City", "To City *"),
        ]

        row = 1
        col_offset = 0
        for key, label in fields:
            ttk.Label(form, text=label, style="TLabel").grid(
                row=row, column=col_offset, sticky="w", padx=(0, 8), pady=4
            )
            var = tk.StringVar()
            self.field_vars[key] = var
            ttk.Entry(form, textvariable=var, style="TEntry").grid(
                row=row, column=col_offset + 1,
                sticky="ew", padx=(0, 20), pady=4,
            )
            if col_offset == 0:
                col_offset = 2
            else:
                col_offset = 0
                row += 1

        if col_offset == 2:
            row += 1

    def _build_table(self, parent: ttk.Frame) -> None:
        table_frame = ttk.Frame(parent, style="TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        col_keys = [c[0] for c in FLIGHT_COLUMNS]
        self.tree = ttk.Treeview(
            table_frame, columns=col_keys, show="headings", selectmode="browse"
        )

        for key, heading, width in FLIGHT_COLUMNS:
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
        col_keys = [c[0] for c in FLIGHT_COLUMNS]
        for record in get_flights(self.records):
            self.tree.insert(
                "", "end", values=[record.get(k, "") for k in col_keys]
            )
