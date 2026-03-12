# GUI tab for managing client records.
# Form panel with StringVar-bound fields and a Treeview table.

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict

from app.models.client import (
    create_client, validate_client, get_clients,
    update_client, delete_client, search_clients,
)
from app.models.id_generator import get_next_id

# (dict_key, label_text, required)
CLIENT_FIELDS = [
    ("Name", "Name", True),
    ("Address Line 1", "Address Line 1", True),
    ("Address Line 2", "Address Line 2", False),
    ("Address Line 3", "Address Line 3", False),
    ("City", "City", True),
    ("State", "State", False),
    ("Zip Code", "Zip Code", False),
    ("Country", "Country", True),
    ("Phone", "Phone Number", True),
]

# (key, heading, width)
CLIENT_COLUMNS = [
    ("ID", "ID", 50),
    ("Name", "Name", 140),
    ("Address Line 1", "Addr 1", 120),
    ("City", "City", 90),
    ("State", "State", 70),
    ("Zip Code", "Zip", 60),
    ("Country", "Country", 80),
    ("Phone", "Phone", 110),
]


class ClientTab:
    """Client record management tab with form and data table.

    Provides a complete GUI interface for managing client records including
    a multi-field form, search functionality, and a sortable data table.
    Handles all CRUD operations for client data.

    Attributes:
        parent: Parent ttk.Frame containing this tab.
        records: Shared list of all record dictionaries.
        field_vars: Dictionary mapping field names to StringVar instances.
        selected_id: ID of currently selected client record or None.
        search_var: StringVar for the search input field.
        tree: ttk.Treeview widget displaying client records.
    """

    def __init__(self, parent: ttk.Frame, records: List[Dict]) -> None:
        """Initialise the client tab interface.

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
        """Build the client form with input fields and action buttons.

        Creates a two-column form layout with entry fields for all client
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
            form_wrapper, text="Client Details", style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        # lay fields in two columns, alternating left/right
        row = 1
        col_offset = 0
        for i, (key, label, required) in enumerate(CLIENT_FIELDS):
            display = f"{label} *" if required else label

            ttk.Label(
                form_wrapper, text=display, style="TLabel"
            ).grid(row=row, column=col_offset, sticky="w", padx=(0, 8), pady=4)

            var = tk.StringVar()
            self.field_vars[key] = var
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

        # search bar
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

        # action buttons
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
        """Build the client data table with vertical scrollbar.

        Creates a ttk.Treeview widget displaying client records with
        row selection functionality and a vertical scrollbar.

        Args:
            parent: Parent frame to contain the table widget.
        """
        table_frame = ttk.Frame(parent, style="TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        col_keys = [c[0] for c in CLIENT_COLUMNS]

        self.tree = ttk.Treeview(
            table_frame,
            columns=col_keys,
            show="headings",
            selectmode="browse",
        )

        for key, heading, width in CLIENT_COLUMNS:
            self.tree.heading(key, text=heading, anchor="w")
            self.tree.column(key, width=width, anchor="w", minwidth=40)

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _on_save(self) -> None:
        """Save a new client record with validation.

        Validates form inputs, generates a new ID, creates the client record,
        appends to records list, clears the form, and refreshes the table.
        Shows error message if validation fails.
        """
        values = {k: v.get().strip() for k, v in self.field_vars.items()}

        valid, msg = validate_client(
            values["Name"], values["Address Line 1"],
            values["City"], values["Country"], values["Phone"],
        )
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return

        new_id = get_next_id(self.records, "Client")
        record = create_client(
            new_id,
            values["Name"], values["Address Line 1"],
            values["Address Line 2"], values["Address Line 3"],
            values["City"], values["State"], values["Zip Code"],
            values["Country"], values["Phone"],
        )
        self.records.append(record)
        self._clear_form()
        self.refresh_table()

    def _on_update(self) -> None:
        """Update an existing client record with validation.

        Validates that a record is selected and form inputs are valid,
        updates the record, clears the form, and refreshes the table.
        Shows warning if no record selected or error if validation fails.
        """
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a record to update.")
            return

        values = {k: v.get().strip() for k, v in self.field_vars.items()}

        valid, msg = validate_client(
            values["Name"], values["Address Line 1"],
            values["City"], values["Country"], values["Phone"],
        )
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return

        update_client(self.records, self.selected_id, values)
        self._clear_form()
        self.refresh_table()

    def _on_delete(self) -> None:
        """Delete a client record with confirmation.

        Validates that a record is selected, prompts for confirmation,
        deletes the record, clears the form, and refreshes the table.
        Shows warning if no record is selected.
        """
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a record to delete.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?",
        )
        if confirm:
            delete_client(self.records, self.selected_id)
            self._clear_form()
            self.refresh_table()

    def _on_search(self) -> None:
        """Search client records by any field.

        Executes case-insensitive search across all client fields using
        the search term and updates the table to show matching records.
        If search term is empty, shows all records.
        """
        term = self.search_var.get().strip()
        if not term:
            self.refresh_table()
            return

        results = search_clients(self.records, term)
        self._populate_table(results)

    def _on_row_select(self, event) -> None:
        """Handle row selection to populate form fields.

        When a row is selected in the table, looks up the full record
        and populates all form fields including those not shown in the table.

        Args:
            event: TreeviewSelect event (unused).
        """
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item["values"]
        col_keys = [c[0] for c in CLIENT_COLUMNS]

        row_data = dict(zip(col_keys, values))
        self.selected_id = row_data.get("ID")

        # Look up the full record so fields not shown in the table
        # (Address Line 2, Address Line 3) are populated correctly.
        full_record = {}
        for record in self.records:
            if record.get("ID") == self.selected_id:
                full_record = record
                break

        for key, var in self.field_vars.items():
            var.set(str(full_record.get(key, "")))

    def _clear_form(self) -> None:
        """Clear all form fields and deselect table row.

        Resets the selected_id, clears all field values and the search field.
        """
        self.selected_id = None
        for var in self.field_vars.values():
            var.set("")
        self.search_var.set("")

    def refresh_table(self) -> None:
        """Refresh the table to show all client records.

        Retrieves all client records from the shared records list and
        populates the table display.
        """
        clients = get_clients(self.records)
        self._populate_table(clients)

    def _populate_table(self, data: List[Dict]) -> None:
        """Populate the table with client data.

        Clears the current table contents and inserts rows for each
        client record in the provided data list.

        Args:
            data: List of client record dictionaries to display.
        """
        self.tree.delete(*self.tree.get_children())
        col_keys = [c[0] for c in CLIENT_COLUMNS]

        for record in data:
            row_values = [record.get(k, "") for k in col_keys]
            self.tree.insert("", "end", values=row_values)
