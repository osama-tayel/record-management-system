"""
Client model for the Travel Record Management System.

Provides CRUD and search operations for client records.
"""

from typing import List, Dict, Tuple, Any

# Constant to avoid repeating the string literal                                                
CLIENT_TYPE = "Client"

# Type alias for record dictionaries                                   
Record = Dict[str, Any]


def create_client(
    client_id: int,
    name: str,
    addr1: str,
    addr2: str,
    addr3: str,
    city: str,
    state: str,
    zip_code: str,
    country: str,
    phone: str
) -> Record:
    """Create and return a client record.

    Args:
        client_id: Unique identifier for the client.
        name: Client's full name.
        addr1: Primary address line.
        addr2: Secondary address line (optional).
        addr3: Tertiary address line (optional).
        city: City name.
        state: State or province (optional).
        zip_code: Postal or ZIP code (optional).
        country: Country name.
        phone: Phone number.

    Returns:
        Dictionary containing the complete client record.
    """
    return {
        "ID": client_id,
        "Type": CLIENT_TYPE,
        "Name": name,
        "Address Line 1": addr1,
        "Address Line 2": addr2,
        "Address Line 3": addr3,
        "City": city,
        "State": state,
        "Zip Code": zip_code,
        "Country": country,
        "Phone": phone
    }


def validate_client(
    name: str,
    addr1: str,
    city: str,
    country: str,
    phone: str
) -> Tuple[bool, str]:
    """Validate required client fields.

    Args:
        name: Client's full name.
        addr1: Primary address line.
        city: City name.
        country: Country name.
        phone: Phone number.

    Returns:
        Tuple of (is_valid, error_message). If validation passes, returns
        (True, ""). If validation fails, returns (False, error_message).
    """
    name = name.strip()
    addr1 = addr1.strip()
    city = city.strip()
    country = country.strip()
    phone = phone.strip()

    if not name:
        return False, "Name is required."
    if not addr1:
        return False, "Address Line 1 is required."
    if not city:
        return False, "City is required."
    if not country:
        return False, "Country is required."
    if not phone:
        return False, "Phone is required."

    return True, ""


def check_duplicate_client(
    records: List[Record], name: str, phone: str
) -> bool:
    """Check if a client with the same name and phone already exists.

    Args:
        records: List of all record dictionaries.
        name: Client name to check.
        phone: Client phone number to check.

    Returns:
        True if a duplicate exists, False otherwise.
    """
    for record in get_clients(records):
        if (record.get("Name", "").lower() == name.lower()
                and record.get("Phone", "").lower() == phone.lower()):
            return True
    return False


def get_clients(records: List[Record]) -> List[Record]:
    """Return all client records.

    Args:
        records: List of all record dictionaries.

    Returns:
        Filtered list containing only client records.
    """
    return [record for record in records if record.get("Type") == CLIENT_TYPE]


def update_client(
    records: List[Record],
    client_id: int,
    updated_data: Record
) -> bool:
    """Update a client record by ID.

    Args:
        records: List of all record dictionaries.
        client_id: ID of the client record to update.
        updated_data: Dictionary containing fields to update.

    Returns:
        True if the record was found and updated, False otherwise.
    """
    for record in records:
        if record.get("ID") == client_id and record.get("Type") == CLIENT_TYPE:
            record.update(updated_data)
            return True

    return False


def delete_client(records: List[Record], client_id: int) -> bool:
    """Delete a client record by ID.

    Args:
        records: List of all record dictionaries.
        client_id: ID of the client record to delete.

    Returns:
        True if the record was found and deleted, False otherwise.
    """
    for i, record in enumerate(records):
        if record.get("ID") == client_id and record.get("Type") == CLIENT_TYPE:
            records.pop(i)
            return True

    return False


def search_clients(records: List[Record], search_term: str) -> List[Record]:
    """Search client records by any field (case-insensitive).

    Args:
        records: List of all record dictionaries.
        search_term: String to search for across all fields.

    Returns:
        List of client records containing the search term in any field.
    """
    search_term = search_term.lower()

    return [
        record for record in records
        if record.get("Type") == CLIENT_TYPE
        and any(search_term in str(value).lower() for value in record.values())
    ]
