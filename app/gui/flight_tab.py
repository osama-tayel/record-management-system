# GUI tab for managing flight records.
# Complete CRUD implementation with date and ID validation.

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict

from app.models.flight import (
    create_flight, validate_flight, get_flights,
    update_flight, delete_flight, search_flights,
    validate_foreign_keys, check_duplicate_flight,
)
from app.models.client import get_clients
from app.models.airline import get_airlines
from app.models.id_generator import get_next_id
from app.storage.json_storage import StorageManager
from app.gui.autocomplete import AutocompleteEntry

# (key, heading, width)
FLIGHT_COLUMNS = [
    ("ID", "ID", 40),
    ("Client_ID", "Client ID", 60),
    ("Client_Name", "Client Name", 140),
    ("Airline_Name", "Airline Name", 140),
    ("Date", "Date", 90),
    ("Start City", "From", 100),
    ("End City", "To", 100),
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

    def __init__(
        self, parent: ttk.Frame, records: List[Dict],
        storage: StorageManager = None
    ) -> None:
        """Initialise the flight tab interface.

        Args:
            parent: Parent ttk.Frame to contain this tab's widgets.
            records: Shared list of all record dictionaries.
            storage: StorageManager instance for immediate persistence.
        """
        self.parent = parent
        self.records = records
        self.storage = storage
        self.field_vars: Dict[str, tk.StringVar] = {}
        self.selected_id = None

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        self._build_form(parent)
        self._build_table(parent)
        self._refresh_combos()
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

        # Client dropdown
        ttk.Label(form_wrapper, text="Client *", style="TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=4
        )
        self._client_var = tk.StringVar()
        self._client_combo = ttk.Combobox(
            form_wrapper, textvariable=self._client_var, state="readonly"
        )
        self._client_combo.grid(
            row=1, column=1, sticky="ew", padx=(0, 20), pady=4
        )

        # Airline dropdown
        ttk.Label(form_wrapper, text="Airline *", style="TLabel").grid(
            row=1, column=2, sticky="w", padx=(0, 8), pady=4
        )
        self._airline_var = tk.StringVar()
        self._airline_combo = ttk.Combobox(
            form_wrapper, textvariable=self._airline_var, state="readonly"
        )
        self._airline_combo.grid(
            row=1, column=3, sticky="ew", padx=(0, 0), pady=4
        )

        # Remaining text fields with autocomplete on cities
        text_fields = [
            ("Date", "Date (YYYY-MM-DD) *"),
            ("Start City", "From City *"),
            ("End City", "To City *"),
        ]

        ac_callbacks = {
            "Start City": lambda: sorted({
                r.get("Start City", "") for r in get_flights(self.records)
                if r.get("Start City")
            } | {
                r.get("City", "") for r in get_clients(self.records)
                if r.get("City")
            }),
            "End City": lambda: sorted({
                r.get("End City", "") for r in get_flights(self.records)
                if r.get("End City")
            } | {
                r.get("City", "") for r in get_clients(self.records)
                if r.get("City")
            }),
        }

        row = 2
        col_offset = 0
        for key, label in text_fields:
            ttk.Label(form_wrapper, text=label, style="TLabel").grid(
                row=row, column=col_offset, sticky="w", padx=(0, 8), pady=4
            )
            var = tk.StringVar()
            self.field_vars[key] = var

            if key in ac_callbacks:
                entry = AutocompleteEntry(
                    form_wrapper, textvariable=var,
                    get_suggestions=ac_callbacks[key], style="TEntry"
                )
            else:
                entry = ttk.Entry(form_wrapper, textvariable=var, style="TEntry")

            entry.grid(
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

    def _refresh_combos(self):
        """Refresh the client and airline dropdown options."""
        self._client_options = {
            r.get("Name", ""): r["ID"] for r in get_clients(self.records)
        }
        self._airline_options = {
            r.get("Company Name", ""): r["ID"] for r in get_airlines(self.records)
        }
        self._client_combo["values"] = list(self._client_options.keys())
        self._airline_combo["values"] = list(self._airline_options.keys())

    def _parse_form_values(self):
        """Parse and validate form values from dropdowns and text fields.

        Returns:
            Tuple of (client_id, airline_id, flight_date, start_city, end_city)
            or None if validation fails.
        """
        client_name = self._client_var.get()
        airline_name = self._airline_var.get()

        if not client_name:
            messagebox.showerror("Validation Error", "Please select a client.")
            return None
        if not airline_name:
            messagebox.showerror("Validation Error", "Please select an airline.")
            return None

        client_id = self._client_options.get(client_name)
        airline_id = self._airline_options.get(airline_name)

        if client_id is None:
            messagebox.showerror("Validation Error", "Selected client not found.")
            return None
        if airline_id is None:
            messagebox.showerror("Validation Error", "Selected airline not found.")
            return None

        flight_date = self.field_vars["Date"].get().strip()
        start_city = self.field_vars["Start City"].get().strip()
        end_city = self.field_vars["End City"].get().strip()

        valid, msg = validate_flight(
            client_id, airline_id, flight_date, start_city, end_city
        )
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return None

        return client_id, airline_id, flight_date, start_city, end_city

    def _on_save(self) -> None:
        """Save a new flight record with validation.

        Validates Client_ID and Airline_ID as integers, checks they reference
        existing records, validates date format as ISO YYYY-MM-DD, checks for
        duplicate flights, generates a new ID, creates the flight record,
        and refreshes the table. Shows error messages if validation fails.
        """
        if self.selected_id is not None:
            messagebox.showwarning(
                "Record Selected",
                "A record is currently selected. Use 'Update' to modify it, "
                "or 'Clear' the form first to add a new record."
            )
            return

        # Parse form values (handle "1 - Name" autocomplete format)
        parsed = self._parse_form_values()
        if parsed is None:
            return

        client_id, airline_id, flight_date, start_city, end_city = parsed

        # Check for duplicate flights
        if check_duplicate_flight(
            self.records, client_id, airline_id,
            flight_date, start_city, end_city
        ):
            messagebox.showerror(
                "Duplicate",
                "A flight with the same details already exists."
            )
            return

        # Generate next ID and create record
        new_id = get_next_id(self.records, "Flight")
        record = create_flight(
            new_id, client_id, airline_id,
            flight_date, start_city, end_city
        )
        self.records.append(record)
        if self.storage:
            self.storage.save(self.records)
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

        # Parse form values (handle "1 - Name" autocomplete format)
        parsed = self._parse_form_values()
        if parsed is None:
            return

        client_id, airline_id, flight_date, start_city, end_city = parsed

        # Update record
        updated_data = {
            "Client_ID": client_id,
            "Airline_ID": airline_id,
            "Date": flight_date,
            "Start City": start_city,
            "End City": end_city,
        }
        update_flight(self.records, self.selected_id, updated_data)
        if self.storage:
            self.storage.save(self.records)
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
            if self.storage:
                self.storage.save(self.records)
            self._clear_form()
            self.refresh_table()
            messagebox.showinfo("Success", "Flight record deleted.")

    def _on_search(self) -> None:
        """Search flight records by any field including resolved names.

        Searches across all flight fields plus the client name and airline
        name (resolved from IDs). Case-insensitive. If search term is empty,
        shows all records.
        """
        term = self.search_var.get().strip().lower()
        if not term:
            self.refresh_table()
            return

        results = []
        for record in get_flights(self.records):
            client_name = self._lookup_client_name(
                record.get("Client_ID")
            ).lower()
            airline_name = self._lookup_airline_name(
                record.get("Airline_ID")
            ).lower()

            searchable = [
                str(record.get("ID", "")),
                str(record.get("Client_ID", "")),
                client_name,
                airline_name,
                record.get("Date", ""),
                record.get("Start City", ""),
                record.get("End City", ""),
            ]

            if any(term in field.lower() for field in searchable):
                results.append(record)

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

        # Look up the full record to populate form fields
        full_record = {}
        for record in self.records:
            if (record.get("ID") == self.selected_id
                    and record.get("Type") == "Flight"):
                full_record = record
                break

        # Set combobox selections by looking up names from IDs
        client_name = self._lookup_client_name(full_record.get("Client_ID"))
        airline_name = self._lookup_airline_name(full_record.get("Airline_ID"))
        self._client_var.set(client_name)
        self._airline_var.set(airline_name)

        for key in ["Date", "Start City", "End City"]:
            self.field_vars[key].set(str(full_record.get(key, "")))

    def _clear_form(self) -> None:
        """Clear all form fields and deselect table row.

        Resets the selected_id, clears all field values, comboboxes,
        and the search field.
        """
        self.selected_id = None
        self._client_var.set("")
        self._airline_var.set("")
        for var in self.field_vars.values():
            var.set("")
        self.search_var.set("")
        self._refresh_combos()

    def refresh_table(self) -> None:
        """Refresh the table to show all flight records.

        Retrieves all flight records from the shared records list and
        populates the table display.
        """
        flights = get_flights(self.records)
        self._populate_table(flights)

    def _lookup_client_name(self, client_id) -> str:
        """Look up client name by ID for display in the table."""
        for r in get_clients(self.records):
            if r.get("ID") == client_id:
                return r.get("Name", "")
        return ""

    def _lookup_airline_name(self, airline_id) -> str:
        """Look up airline company name by ID for display in the table."""
        for r in get_airlines(self.records):
            if r.get("ID") == airline_id:
                return r.get("Company Name", "")
        return ""

    def _populate_table(self, data: List[Dict]) -> None:
        """Populate the table with flight data.

        Resolves Client_ID and Airline_ID to display names in separate columns.

        Args:
            data: List of flight record dictionaries to display.
        """
        self.tree.delete(*self.tree.get_children())

        for record in data:
            client_id = record.get("Client_ID", "")
            airline_id = record.get("Airline_ID", "")
            row_values = [
                record.get("ID", ""),
                client_id,
                self._lookup_client_name(client_id),
                self._lookup_airline_name(airline_id),
                record.get("Date", ""),
                record.get("Start City", ""),
                record.get("End City", ""),
            ]
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
