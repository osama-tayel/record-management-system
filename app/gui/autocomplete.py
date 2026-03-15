# Reusable autocomplete entry widget for Tkinter.
# Shows a dropdown of suggestions as the user types.

import tkinter as tk
from tkinter import ttk
from typing import Callable, List


class AutocompleteEntry(ttk.Entry):
    """Entry widget with dropdown autocomplete suggestions.

    Displays a floating listbox below the entry that filters suggestions
    as the user types. Selecting a suggestion fills the entry field.

    Attributes:
        get_suggestions: Callback returning list of suggestion strings.
        _listbox: Toplevel listbox showing filtered suggestions.
    """

    def __init__(self, parent, textvariable, get_suggestions: Callable[[], List[str]],
                 **kwargs):
        """Initialise the autocomplete entry.

        Args:
            parent: Parent widget.
            textvariable: StringVar bound to this entry.
            get_suggestions: Callable returning current list of suggestions.
            **kwargs: Additional keyword arguments passed to ttk.Entry.
        """
        super().__init__(parent, textvariable=textvariable, **kwargs)
        self.var = textvariable
        self.get_suggestions = get_suggestions
        self._listbox = None
        self._updating = False

        self.var.trace_add("write", self._on_change)
        self.bind("<Down>", self._on_arrow_down)
        self.bind("<Escape>", self._close_listbox)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_change(self, *args):
        """Filter and display suggestions when text changes."""
        if self._updating:
            return

        typed = self.var.get().strip().lower()
        if not typed:
            self._close_listbox()
            return

        matches = [s for s in self.get_suggestions() if typed in s.lower()]

        if not matches:
            self._close_listbox()
            return

        self._show_listbox(matches)

    def _show_listbox(self, items):
        """Show or update the dropdown listbox with matching items."""
        if self._listbox:
            self._listbox.destroy()

        lb_window = tk.Toplevel(self)
        lb_window.wm_overrideredirect(True)
        lb_window.attributes("-topmost", True)

        listbox = tk.Listbox(lb_window, height=min(len(items), 6),
                             selectmode="browse", activestyle="none")
        for item in items:
            listbox.insert("end", item)

        listbox.pack(fill="both", expand=True)
        listbox.bind("<<ListboxSelect>>", self._on_select)
        listbox.bind("<Return>", self._on_select)

        # Position below the entry widget
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        w = self.winfo_width()
        lb_window.geometry(f"{w}x{min(len(items), 6) * 20}+{x}+{y}")

        self._listbox = lb_window

    def _on_select(self, event):
        """Handle selection from the listbox."""
        widget = event.widget
        if not widget.curselection():
            return

        value = widget.get(widget.curselection()[0])
        self._updating = True
        self.var.set(value)
        self._updating = False
        self._close_listbox()
        self.icursor("end")

    def _on_arrow_down(self, event):
        """Move focus to listbox when pressing down arrow."""
        if self._listbox:
            listbox = self._listbox.winfo_children()[0]
            listbox.focus_set()
            listbox.selection_set(0)

    def _on_focus_out(self, event):
        """Close listbox when entry loses focus (with delay for click)."""
        self.after(150, self._close_listbox)

    def _close_listbox(self, event=None):
        """Destroy the dropdown listbox."""
        if self._listbox:
            self._listbox.destroy()
            self._listbox = None
