# Simple ttk styling for the Record Management System.

import tkinter as tk
from tkinter import ttk

# colours
BG = "#F5F5F5"
FG = "#1C1B1D"
PRIMARY = "#6442D6"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#E8E8E8"
RED = "#D32F2F"

FONT = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_HEADING = ("Segoe UI", 16, "bold")


def apply_theme(root: tk.Tk) -> ttk.Style:
    """Set up the clam theme with colour and font overrides.

    Configures ttk widget styles with custom colours, fonts, and behaviours
    for the application. Uses the 'clam' theme as a foundation and applies
    custom styling for frames, labels, buttons, entries, notebook tabs,
    and treeviews.

    Args:
        root: The root Tkinter window to apply the theme to.

    Returns:
        Configured ttk.Style instance.
    """
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=FG, font=FONT)
    style.configure("Heading.TLabel", font=FONT_HEADING, foreground=PRIMARY, background=BG)
    style.configure("Title.TLabel", font=FONT_BOLD, foreground=FG, background=BG)

    style.configure("TEntry", padding=(8, 6), font=FONT)
    style.map("TEntry", bordercolor=[("focus", PRIMARY)])

    style.configure("TButton", font=FONT_BOLD, padding=(14, 7))
    style.configure("Primary.TButton", background=PRIMARY, foreground=WHITE, font=FONT_BOLD, padding=(14, 7))
    style.map("Primary.TButton", background=[("active", "#5635C0")])
    style.configure("Danger.TButton", background=RED, foreground=WHITE, font=FONT_BOLD, padding=(14, 7))
    style.map("Danger.TButton", background=[("active", "#B71C1C")])

    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", font=FONT_BOLD, padding=(18, 8))
    style.map("TNotebook.Tab", foreground=[("selected", PRIMARY)])

    style.configure("Treeview", font=FONT, rowheight=30)
    style.configure("Treeview.Heading", font=FONT_BOLD)
    style.map("Treeview", background=[("selected", LIGHT_GRAY)])

    return style
