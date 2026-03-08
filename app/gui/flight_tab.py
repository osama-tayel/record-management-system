feature/gui-shell
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
     main
