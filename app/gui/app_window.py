# Main application window with tabbed interface.
# Sets up the Tk root, theme, Notebook tabs, and save-on-close handler.

import tkinter as tk
from tkinter import ttk

from app.gui.theme import apply_theme, BG
from app.gui.client_tab import ClientTab
from app.gui.airline_tab import AirlineTab
from app.gui.flight_tab import FlightTab
from app.storage.json_storage import StorageManager


class AppWindow:
    """Main application window with tabbed navigation for record types."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Travel Agent Record Manager")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        apply_theme(self.root)

        self.storage = StorageManager()
        self.records = self.storage.load()

        self._build_header()
        self._build_notebook()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_header(self) -> None:
        header = ttk.Frame(self.root, style="TFrame")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 4))

        ttk.Label(
            header,
            text="Travel Agent Record Manager",
            style="Heading.TLabel",
        ).grid(row=0, column=0, sticky="w")

        self.root.columnconfigure(0, weight=1)

    def _build_notebook(self) -> None:
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(
            row=1, column=0, sticky="nsew", padx=24, pady=(8, 24)
        )
        self.root.rowconfigure(1, weight=1)

        client_frame = ttk.Frame(self.notebook, style="TFrame")
        self.client_tab = ClientTab(client_frame, self.records)
        self.notebook.add(client_frame, text="  Clients  ")

        airline_frame = ttk.Frame(self.notebook, style="TFrame")
        self.airline_tab = AirlineTab(airline_frame, self.records)
        self.notebook.add(airline_frame, text="  Airlines  ")

        flight_frame = ttk.Frame(self.notebook, style="TFrame")
        self.flight_tab = FlightTab(flight_frame, self.records)
        self.notebook.add(flight_frame, text="  Flights  ")

    def _on_close(self) -> None:
        self.storage.save(self.records)
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()
