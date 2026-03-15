# Record Management System

**CSCK541 Software Development in Practice**
**Group C**

## About

A desktop application for a specialist travel agent to manage their day-to-day business records. The system handles three core entity types that a travel agency relies on: **clients** (the customers booking trips), **airlines** (the carriers operating flights), and **flights** (the actual journeys linking a client to an airline on a given date and route).

Staff can create new records, search and filter existing ones, update details, and delete entries, all through a tabbed graphical interface. Data is persisted immediately to a JSON file on every create, update, and delete operation, so nothing is lost between sessions.

Built entirely with the Python standard library (Tkinter for the GUI, `json` for persistence, `pytest` for testing).

## Features

- **Client Management**: Add, search, update, and delete customer records (name, full address, phone number)
- **Airline Management**: Add, search, update, and delete airline company records
- **Flight Management**: Book and manage flights linking a client to an airline with date and route (start/end city)
- **Tabbed Interface**: Separate tabs for each record type, with form inputs and a searchable data table
- **Auto-increment IDs**: Client and Airline IDs are generated automatically
- **Immediate Persistence**: Data saved to JSON on every create, update, and delete; handles first-run gracefully
- **Data Integrity**: Duplicate detection, foreign key validation, and required field checks enforced at the model layer

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
│   │   ├── flight.py        # Flight data model
│   │   └── id_generator.py  # Auto-increment ID utility
│   ├── storage/
│   │   └── json_storage.py  # JSON file persistence
│   └── gui/
│       ├── app_window.py    # Main window with tabbed navigation
│       ├── theme.py         # ttk colour and font styling
│       ├── client_tab.py    # Client form + table
│       ├── airline_tab.py   # Airline form + table
│       └── flight_tab.py    # Flight form + table
├── tests/
│   ├── test_client.py       # Client model tests
│   ├── test_airline.py      # Airline model tests
│   ├── test_flight.py       # Flight model tests
│   ├── test_gui_logic.py    # GUI logic tests
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
git clone https://github.com/ahmed-osama-tayel/record-management-system.git
cd record-management-system

# Run the application
python -m app.main

# Run the test suite
python -m pytest tests/
```

## Team

| Name | Role |
|------|------|
| Ahmed Tayel | Project Manager & Designer |
| Callum Blanshard | Tester |
| Chadé Smith | Designer |
| Christopher Lloyd | Engineer |
| Fouzia Farqan | Engineer |
