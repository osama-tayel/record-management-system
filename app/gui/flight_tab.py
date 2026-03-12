# GUI tab for managing flight records.
# Complete CRUD implementation with date and ID validation.

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
from datetime import date

from app.models.flight import (
    create_flight, validate_flight, get_flights,
    update_flight, delete_flight, search_flights,
)
from app.models.id_generator import get_next_id

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
    """Flight record management tab with full CRUD operations.

    Provides a GUI interface for managing flight records with form inputs,
    search functionality, and a sortable data table. Includes comprehensive
    validation for date formats and foreign key IDs.

    Attributes:
        parent: Parent ttk.Frame containing this tab.
        records: Shared list of all record dictionaries.
        field_vars: Dictionary mapping field names to StringVar instances.
        selected_id: ID of currently selected flight record or None.
        search_var: StringVar for the search input field.
        tree: ttk.Treeview widget displaying flight records.
    """

    def __init__(self, parent: ttk.Frame, records: List[Dict]) -> None:
        """Initialise the flight tab interface.

        Args:
            parent: Parent ttk.Frame to contain this tab's widgets.
            records: Shared list of all record dictionaries.
        """
        self.parent = parent
        self.records = records
        self.field_vars: Dict[str, tk.StringVar] = {}
        self.selected_id = None

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        self._build_form(parent)
        self._build_table(parent)
        self.refresh_table()

    def _build_form(self, parent: ttk.Frame) -> None:
        """Build the flight form with fields and buttons.

        Creates a two-column form layout with entry fields for flight
        attributes, a search bar, and buttons for Save, Update, Delete,
        and Clear operations.

        Args:
            parent: Parent frame to contain the form widgets.
        """
        form_wrapper = ttk.Frame(parent, style="TFrame")
        form_wrapper.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        form_wrapper.columnconfigure(1, weight=1)
        form_wrapper.columnconfigure(3, weight=1)

        ttk.Label(
            form_wrapper, text="Flight Details", style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        # Form fields in two columns
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
            ttk.Label(form_wrapper, text=label, style="TLabel").grid(
                row=row, column=col_offset, sticky="w", padx=(0, 8), pady=4
            )
            var = tk.StringVar()
            self.field_vars[key] = var
            ttk.Entry(form_wrapper, textvariable=var, style="TEntry").grid(
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

        # Search bar
        search_frame = ttk.Frame(form_wrapper, style="TFrame")
        search_frame.grid(
            row=row, column=0, columnspan=4, sticky="ew", pady=(12, 0)
        )
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search", style="TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.search_var = tk.StringVar()
        ttk.Entry(
            search_frame, textvariable=self.search_var, style="TEntry"
        ).grid(row=0, column=1, sticky="ew", padx=(0, 8))

        ttk.Button(
            search_frame, text="Search", style="TButton",
            command=self._on_search,
        ).grid(row=0, column=2, padx=(0, 4))

        ttk.Button(
            search_frame, text="Show All", style="TButton",
            command=self.refresh_table,
        ).grid(row=0, column=3)

        row += 1

        # Action buttons
        btn_frame = ttk.Frame(form_wrapper, style="TFrame")
        btn_frame.grid(
            row=row, column=0, columnspan=4, sticky="e", pady=(12, 0)
        )

        ttk.Button(
            btn_frame, text="Save", style="Primary.TButton",
            command=self._on_save,
        ).grid(row=0, column=0, padx=(0, 8))

        ttk.Button(
            btn_frame, text="Update", style="TButton",
            command=self._on_update,
        ).grid(row=0, column=1, padx=(0, 8))

        ttk.Button(
            btn_frame, text="Delete", style="Danger.TButton",
            command=self._on_delete,
        ).grid(row=0, column=2, padx=(0, 8))

        ttk.Button(
            btn_frame, text="Clear", style="TButton",
            command=self._clear_form,
        ).grid(row=0, column=3)

    def _build_table(self, parent: ttk.Frame) -> None:
        """Build the flight data table with sorting.

        Creates a ttk.Treeview widget displaying flight records with
        sortable columns, row selection functionality, and a vertical scrollbar.

        Args:
            parent: Parent frame to contain the table widget.
        """
        table_frame = ttk.Frame(parent, style="TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        col_keys = [c[0] for c in FLIGHT_COLUMNS]

        self.tree = ttk.Treeview(
            table_frame,
            columns=col_keys,
            show="headings",
            selectmode="browse",
        )

        for key, heading, width in FLIGHT_COLUMNS:
            self.tree.heading(
                key,
                text=heading,
                anchor="w",
                command=lambda c=key: self._sort_column(c, False)
            )
            self.tree.column(key, width=width, anchor="w", minwidth=40)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _on_save(self) -> None:
        """Save a new flight record with validation.

        Validates Client_ID and Airline_ID as integers, validates date format
        as ISO YYYY-MM-DD, validates other required fields, generates a new ID,
        creates the flight record, and refreshes the table. Shows error messages
        if validation fails.
        """
        # Get form values
        client_id_str = self.field_vars["Client_ID"].get().strip()
        airline_id_str = self.field_vars["Airline_ID"].get().strip()
        flight_date = self.field_vars["Date"].get().strip()
        start_city = self.field_vars["Start City"].get().strip()
        end_city = self.field_vars["End City"].get().strip()

        # Validate Client_ID is an integer
        try:
            client_id = int(client_id_str)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Client ID must be a valid integer."
            )
            return

        # Validate Airline_ID is an integer
        try:
            airline_id = int(airline_id_str)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Airline ID must be a valid integer."
            )
            return

        # Validate date format using date.fromisoformat()
        try:
            date.fromisoformat(flight_date)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Date must be in YYYY-MM-DD format (e.g., 2026-03-15)."
            )
            return

        # Validate using flight model validation
        valid, msg = validate_flight(
            client_id, airline_id, flight_date, start_city, end_city
        )
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return

        # Generate next ID and create record
        new_id = get_next_id(self.records, "Flight")
        record = create_flight(
            new_id, client_id, airline_id,
            flight_date, start_city, end_city
        )
        self.records.append(record)
        self._clear_form()
        self.refresh_table()
        messagebox.showinfo("Success", "Flight record saved successfully.")

    def _on_update(self) -> None:
        """Update an existing flight record with validation.

        Validates that a record is selected, validates Client_ID and Airline_ID
        as integers, validates date format, validates other required fields,
        updates the record, and refreshes the table. Shows warnings and errors
        if validation fails.
        """
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a record to update.")
            return

        # Get form values
        client_id_str = self.field_vars["Client_ID"].get().strip()
        airline_id_str = self.field_vars["Airline_ID"].get().strip()
        flight_date = self.field_vars["Date"].get().strip()
        start_city = self.field_vars["Start City"].get().strip()
        end_city = self.field_vars["End City"].get().strip()

        # Validate Client_ID is an integer
        try:
            client_id = int(client_id_str)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Client ID must be a valid integer."
            )
            return

        # Validate Airline_ID is an integer
        try:
            airline_id = int(airline_id_str)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Airline ID must be a valid integer."
            )
            return

        # Validate date format
        try:
            date.fromisoformat(flight_date)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Date must be in YYYY-MM-DD format (e.g., 2026-03-15)."
            )
            return

        # Validate using flight model validation
        valid, msg = validate_flight(
            client_id, airline_id, flight_date, start_city, end_city
        )
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return

        # Update record
        updated_data = {
            "Client_ID": client_id,
            "Airline_ID": airline_id,
            "Date": flight_date,
            "Start City": start_city,
            "End City": end_city,
        }
        update_flight(self.records, self.selected_id, updated_data)
        self._clear_form()
        self.refresh_table()
        messagebox.showinfo("Success", "Flight record updated successfully.")

    def _on_delete(self) -> None:
        """Delete a flight record with confirmation.

        Validates that a record is selected, prompts for confirmation,
        deletes the record, clears the form, and refreshes the table.
        Shows warning if no record is selected.
        """
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a record to delete.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this flight record?",
        )
        if confirm:
            delete_flight(self.records, self.selected_id)
            self._clear_form()
            self.refresh_table()
            messagebox.showinfo("Success", "Flight record deleted.")

    def _on_search(self) -> None:
        """Search flight records by any field.

        Executes case-insensitive search across all flight fields using
        the search term and updates the table to show matching records.
        If search term is empty, shows all records.
        """
        term = self.search_var.get().strip()
        if not term:
            self.refresh_table()
            return

        results = search_flights(self.records, term)
        self._populate_table(results)

    def _on_row_select(self, event) -> None:
        """Handle row selection to populate form fields.

        When a row is selected in the table, extracts the flight data
        and populates all form fields with the selected flight's values.

        Args:
            event: TreeviewSelect event (unused).
        """
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item["values"]
        col_keys = [c[0] for c in FLIGHT_COLUMNS]

        row_data = dict(zip(col_keys, values))
        self.selected_id = row_data.get("ID")

        # Populate form fields from selected row
        for key in ["Client_ID", "Airline_ID", "Date", "Start City", "End City"]:
            self.field_vars[key].set(str(row_data.get(key, "")))

    def _clear_form(self) -> None:
        """Clear all form fields and deselect table row.

        Resets the selected_id, clears all field values and the search field.
        """
        self.selected_id = None
        for var in self.field_vars.values():
            var.set("")
        self.search_var.set("")

    def refresh_table(self) -> None:
        """Refresh the table to show all flight records.

        Retrieves all flight records from the shared records list and
        populates the table display.
        """
        flights = get_flights(self.records)
        self._populate_table(flights)

    def _populate_table(self, data: List[Dict]) -> None:
        """Populate the table with flight data.

        Clears the current table contents and inserts rows for each
        flight record in the provided data list.

        Args:
            data: List of flight record dictionaries to display.
        """
        self.tree.delete(*self.tree.get_children())
        col_keys = [c[0] for c in FLIGHT_COLUMNS]

        for record in data:
            row_values = [record.get(k, "") for k in col_keys]
            self.tree.insert("", "end", values=row_values)

    def _sort_column(self, col, reverse):
        """Sort table by column (ascending/descending).

        Sorts the table entries by the specified column, attempting numeric
        sort for ID columns and falling back to string sort otherwise.
        Updates the column heading command to toggle sort direction on next click.

        Args:
            col: Column key to sort by.
            reverse: True for descending order, False for ascending.
        """
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        # Try numeric sort for ID columns, fallback to string sort
        try:
            data.sort(key=lambda x: int(x[0]), reverse=reverse)
        except (ValueError, TypeError):
            data.sort(reverse=reverse)

        for index, (val, k) in enumerate(data):
            self.tree.move(k, "", index)

        self.tree.heading(col, command=lambda: self._sort_column(col, not reverse))
