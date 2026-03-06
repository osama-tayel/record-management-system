"""Flight model representing a scheduled flight.
Provides CRUD operations and validation for flight data.
Dates are stored as ISO strings (YYYY-MM-DD) to avoid JSON serialization issues.
"""

# typing module helps describe expected data structures (for readability and IDE support)
from typing import List, Dict, Tuple, Any

# used to validate ISO date strings
from datetime import date


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
    """
    Create and return a flight record dictionary.
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
    """
    Validate required fields and data types.
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


def get_flights(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Return all records where Type is 'Flight'.
    """

    return [record for record in records if record.get("Type") == FLIGHT_TYPE]


def update_flight(
    records: List[Dict[str, Any]],
    flight_id: int,
    updated_data: Dict[str, Any]
) -> bool:
    """
    Update a flight record by ID.
    """

    for record in records:
        if record.get("ID") == flight_id and record.get("Type") == FLIGHT_TYPE:
            record.update(updated_data)
            return True

    return False


def delete_flight(records: List[Dict[str, Any]], flight_id: int) -> bool:
    """
    Delete a flight record by ID.
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
    """
    Search flight records by any field (case-insensitive).
    """

    # convert search term to lowercase for case-insensitive comparison
    search_term = str(search_term).lower()

    return [
        record
        for record in records
        if record.get("Type") == FLIGHT_TYPE
        and any(search_term in str(value).lower() for value in record.values())
    ]
