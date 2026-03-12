"""
Airline model representing an airline company.

Provides CRUD operations for airline records.
"""

from typing import List, Dict, Tuple, Any

AIRLINE_TYPE = "Airline"


def create_airline(airline_id: int, company_name: str) -> Dict[str, Any]:
    """Create and return an airline record dictionary.

    Args:
        airline_id: Unique identifier for the airline.
        company_name: Name of the airline company.

    Returns:
        Dictionary containing airline record with ID, Type, and Company Name.
    """
    return {
        "ID": airline_id,
        "Type": AIRLINE_TYPE,
        "Company Name": company_name
    }


def validate_airline(company_name: str) -> Tuple[bool, str]:
    """Validate required airline fields.

    Args:
        company_name: Name of the airline company to validate.

    Returns:
        Tuple of (is_valid, error_message). If validation passes, returns
        (True, ""). If validation fails, returns (False, error_message).
    """
    if not company_name or not company_name.strip():
        return False, "Company Name is required."

    return True, ""


def get_airlines(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return all records where Type is 'Airline'.

    Args:
        records: List of all record dictionaries.

    Returns:
        Filtered list containing only airline records.
    """
    return [r for r in records if r.get("Type") == AIRLINE_TYPE]


def update_airline(
    records: List[Dict[str, Any]],
    airline_id: int,
    updated_data: Dict[str, Any]
) -> bool:
    """Update an airline record by ID.

    Args:
        records: List of all record dictionaries.
        airline_id: ID of the airline record to update.
        updated_data: Dictionary containing fields to update.

    Returns:
        True if the record was found and updated, False otherwise.
    """
    for record in records:
        if record.get("ID") == airline_id and record.get("Type") == AIRLINE_TYPE:
            record.update(updated_data)
            return True

    return False


def delete_airline(records: List[Dict[str, Any]], airline_id: int) -> bool:
    """Delete an airline record by ID.

    Args:
        records: List of all record dictionaries.
        airline_id: ID of the airline record to delete.

    Returns:
        True if the record was found and deleted, False otherwise.
    """
    for i, record in enumerate(records):
        if record.get("ID") == airline_id and record.get("Type") == AIRLINE_TYPE:
            records.pop(i)
            return True

    return False


def search_airlines(
    records: List[Dict[str, Any]],
    search_term: str
) -> List[Dict[str, Any]]:
    """Search airline records by any field (case-insensitive).

    Args:
        records: List of all record dictionaries.
        search_term: String to search for across all fields.

    Returns:
        List of airline records containing the search term in any field.
    """
    search_term = search_term.lower()

    return [
        record
        for record in records
        if record.get("Type") == AIRLINE_TYPE
        and any(search_term in str(v).lower() for v in record.values())
    ]
