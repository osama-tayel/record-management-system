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
    """Main application window with tabbed navigation for record types.

    Attributes:
        root: Main Tkinter window instance.
        storage: StorageManager instance for persisting data.
        records: List of all record dictionaries loaded from storage.
        notebook: ttk.Notebook widget containing tab pages.
        client_tab: ClientTab instance managing client records.
        airline_tab: AirlineTab instance managing airline records.
        flight_tab: FlightTab instance managing flight records.
    """

    def __init__(self) -> None:
        """Initialise the application window and load data.

        Creates the main window, applies theme, loads records from storage,
        and builds the header and tabbed interface.
        """
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
        """Build the application header with title label.

        Creates a frame at the top of the window containing the application
        title styled with the Heading.TLabel style.
        """
        header = ttk.Frame(self.root, style="TFrame")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 4))

        ttk.Label(
            header,
            text="Travel Agent Record Manager",
            style="Heading.TLabel",
        ).grid(row=0, column=0, sticky="w")

        self.root.columnconfigure(0, weight=1)

    def _build_notebook(self) -> None:
        """Build the tabbed notebook interface.

        Creates a ttk.Notebook with three tabs: Clients, Airlines, and Flights.
        Each tab contains its respective management interface.
        """
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(
            row=1, column=0, sticky="nsew", padx=24, pady=(8, 24)
        )
        self.root.rowconfigure(1, weight=1)

        client_frame = ttk.Frame(self.notebook, style="TFrame")
        self.client_tab = ClientTab(client_frame, self.records, self.storage)
        self.notebook.add(client_frame, text=" Clients ")

        airline_frame = ttk.Frame(self.notebook, style="TFrame")
        self.airline_tab = AirlineTab(airline_frame, self.records)
        self.notebook.add(airline_frame, text=" Airlines ")

        flight_frame = ttk.Frame(self.notebook, style="TFrame")
        self.flight_tab = FlightTab(flight_frame, self.records, self.storage)
        self.notebook.add(flight_frame, text=" Flights ")

    def _on_close(self) -> None:
        """Handle window close event.

        Saves all records to storage before destroying the window,
        ensuring no data is lost on application exit.
        """
        self.storage.save(self.records)
        self.root.destroy()

    def run(self) -> None:
        """Start the Tkinter main event loop.

        Begins the GUI event processing loop. This method blocks until
        the window is closed.
        """
        self.root.mainloop()
