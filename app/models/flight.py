"""Flight model representing a scheduled flight.

Provides CRUD operations and validation for flight data.
Dates are stored as ISO strings (YYYY-MM-DD) to avoid JSON serialisation issues.
"""

# typing module helps describe expected data structures (for readability and IDE support)
from typing import List, Dict, Tuple, Any

# used to validate ISO date strings
from datetime import date

from app.models.client import get_clients
from app.models.airline import get_airlines

# constant used to identify flight records
FLIGHT_TYPE = "Flight"


def create_flight(
    flight_id: int,
    client_id: int,
    airline_id: int,
    flight_date: str,
    start_city: str,
    end_city: str
) -> Dict[str, Any]:
    """Create and return a flight record dictionary.

    Args:
        flight_id: Unique identifier for the flight.
        client_id: ID of the client associated with this flight.
        airline_id: ID of the airline operating this flight.
        flight_date: Flight date in ISO format (YYYY-MM-DD).
        start_city: Departure city.
        end_city: Arrival city.

    Returns:
        Dictionary containing the complete flight record.
    """
    return {
        "ID": flight_id,
        "Type": FLIGHT_TYPE,
        "Client_ID": client_id,
        "Airline_ID": airline_id,
        "Date": flight_date,  # stored as ISO string for JSON compatibility
        "Start City": start_city.strip(),  # strip removes extra spaces from user input
        "End City": end_city.strip()
    }


def validate_flight(
    client_id: Any,
    airline_id: Any,
    flight_date: str,
    start_city: str,
    end_city: str
) -> Tuple[bool, str]:
    """Validate required fields and data types.

    Args:
        client_id: Client ID to validate (must be integer).
        airline_id: Airline ID to validate (must be integer).
        flight_date: Flight date string to validate (must be ISO format).
        start_city: Departure city to validate.
        end_city: Arrival city to validate.

    Returns:
        Tuple of (is_valid, error_message). If validation passes, returns
        (True, ""). If validation fails, returns (False, error_message).
    """
    # Client_ID must be an integer
    if not isinstance(client_id, int):
        return False, "Client_ID must be an integer."

    # Airline_ID must be an integer
    if not isinstance(airline_id, int):
        return False, "Airline_ID must be an integer."

    # Validate ISO date format using datetime
    try:
        date.fromisoformat(flight_date)
    except ValueError:
        return False, "Date must be in ISO format YYYY-MM-DD."

    # Required field validation
    if not start_city or not start_city.strip():
        return False, "Start City is required."

    if not end_city or not end_city.strip():
        return False, "End City is required."

    return True, ""


def validate_foreign_keys(
    records: List[Dict[str, Any]],
    client_id: int,
    airline_id: int
) -> Tuple[bool, str]:
    """Validate that Client_ID and Airline_ID reference existing records.

    Args:
        records: List of all record dictionaries.
        client_id: Client ID to validate.
        airline_id: Airline ID to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    client_ids = {r["ID"] for r in get_clients(records)}
    if client_id not in client_ids:
        return False, (
            f"Client ID {client_id} does not exist. "
            "Please enter a valid Client ID from the Clients tab."
        )

    airline_ids = {r["ID"] for r in get_airlines(records)}
    if airline_id not in airline_ids:
        return False, (
            f"Airline ID {airline_id} does not exist. "
            "Please enter a valid Airline ID from the Airlines tab."
        )

    return True, ""


def check_duplicate_flight(
    records: List[Dict[str, Any]],
    client_id: int,
    airline_id: int,
    flight_date: str,
    start_city: str,
    end_city: str
) -> bool:
    """Check if a flight with the same details already exists.

    Args:
        records: List of all record dictionaries.
        client_id: Client ID to check.
        airline_id: Airline ID to check.
        flight_date: Flight date string to check.
        start_city: Departure city to check.
        end_city: Arrival city to check.

    Returns:
        True if a duplicate exists, False otherwise.
    """
    for record in get_flights(records):
        if (record.get("Client_ID") == client_id
                and record.get("Airline_ID") == airline_id
                and record.get("Date") == flight_date
                and record.get("Start City", "").lower() == start_city.lower()
                and record.get("End City", "").lower() == end_city.lower()):
            return True
    return False


def get_flights(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return all records where Type is 'Flight'.

    Args:
        records: List of all record dictionaries.

    Returns:
        Filtered list containing only flight records.
    """
    return [record for record in records if record.get("Type") == FLIGHT_TYPE]


def update_flight(
    records: List[Dict[str, Any]],
    flight_id: int,
    updated_data: Dict[str, Any]
) -> bool:
    """Update a flight record by ID.

    Args:
        records: List of all record dictionaries.
        flight_id: ID of the flight record to update.
        updated_data: Dictionary containing fields to update.

    Returns:
        True if the record was found and updated, False otherwise.
    """
    for record in records:
        if record.get("ID") == flight_id and record.get("Type") == FLIGHT_TYPE:
            record.update(updated_data)
            return True

    return False


def delete_flight(records: List[Dict[str, Any]], flight_id: int) -> bool:
    """Delete a flight record by ID.

    Args:
        records: List of all record dictionaries.
        flight_id: ID of the flight record to delete.

    Returns:
        True if the record was found and deleted, False otherwise.
    """
    # enumerate allows us to access index while looping
    for i, record in enumerate(records):
        if record.get("ID") == flight_id and record.get("Type") == FLIGHT_TYPE:
            records.pop(i)  # remove the matching record
            return True

    return False


def search_flights(
    records: List[Dict[str, Any]],
    search_term: str
) -> List[Dict[str, Any]]:
    """Search flight records by any field (case-insensitive).

    Args:
        records: List of all record dictionaries.
        search_term: String to search for across all fields.

    Returns:
        List of flight records containing the search term in any field.
    """
    # convert search term to lowercase for case-insensitive comparison
    search_term = str(search_term).lower()

    return [
        record
        for record in records
        if record.get("Type") == FLIGHT_TYPE
        and any(search_term in str(value).lower() for value in record.values())
    ]
