# Record Management System

**CSCK541 Software Development in Practice** — University of Liverpool (MSc)

## About

A desktop application for a specialist travel agent to manage their day-to-day business records. The system handles three core entity types that a travel agency relies on: **clients** (the customers booking trips), **airlines** (the carriers operating flights), and **flights** (the actual journeys linking a client to an airline on a given date and route).

Staff can create new records, search and filter existing ones, update details, and delete entries — all through a tabbed graphical interface. Data is saved automatically to a JSON file when the application closes and reloaded on the next launch, so nothing is lost between sessions.

Built entirely with the Python standard library (Tkinter for the GUI, `json` for persistence, `unittest` for testing) — no external dependencies required.

## Features

- **Client Management** — Add, search, update, and delete customer records (name, full address, phone number)
- **Airline Management** — Add, search, update, and delete airline company records
- **Flight Management** — Book and manage flights linking a client to an airline with date and route (start/end city)
- **Tabbed Interface** — Separate tabs for each record type, with form inputs and a searchable data table
- **Auto-increment IDs** — Client and Airline IDs are generated automatically
- **Persistent Storage** — JSON file saved on close, loaded on start; handles first-run gracefully
- **Input Validation** — Required fields enforced, with clear error/success messages

## Record Types

| Record | Fields |
|--------|--------|
| **Client** | ID (auto), Type, Name, Address Lines 1-3, City, State, Zip Code, Country, Phone Number |
| **Airline** | ID (auto), Type, Company Name |
| **Flight** | Client_ID, Airline_ID, Date, Start City, End City |

## Project Structure

```
record-management-system/
├── app/
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── client.py        # Client data model
│   │   ├── airline.py       # Airline data model
│   │   └── flight.py        # Flight data model
│   ├── storage/
│   │   └── json_storage.py  # JSON file persistence
│   └── gui/
│       ├── app_window.py    # Main window with tabbed navigation
│       ├── client_tab.py    # Client form + table
│       ├── airline_tab.py   # Airline form + table
│       └── flight_tab.py    # Flight form + table
├── tests/
│   ├── test_client.py       # Client model tests
│   ├── test_airline.py      # Airline model tests
│   ├── test_flight.py       # Flight model tests
│   └── test_storage.py      # Storage round-trip tests
├── data/                    # JSON data files (gitignored)
├── MoM/                     # Meeting minutes
├── requirements.txt
└── README.md
```

## Getting Started

**Prerequisites:** Python 3.10+ (Tkinter is included with standard Python installations)

```bash
# Clone the repository
git clone https://github.com/osama-tayel/record-management-system.git
cd record-management-system

# Run the application
python -m app.main

# Run the test suite
python -m unittest discover -s tests
```

## Team

| Name | Role |
|------|------|
| Ahmed Tayel | Project Manager |
| Christopher Lloyd | Engineer |
| Fouzia Farqan | Engineer |
| Chadé Smith | Designer |
| Callum Blanshard | Tester |

## License

University of Liverpool — CSCK541 coursework. Not for redistribution.
