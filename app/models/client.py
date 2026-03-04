"""Client model representing a travel agent customer.
Provides CRUD operations for client records in the
record management system.
"""

from typing import List, Dict, Tuple

# Constant used to avoid repeating the string "Client"
CLIENT_TYPE = "Client"


def create_client(
    client_id: str,
    name: str,
    addr1: str,
    addr2: str,
    addr3: str,
    city: str,
    state: str,
    zip_code: str,
    country: str,
    phone: str
) -> Dict[str, str]:
    """Create and return a client record dictionary."""

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
    """Validate required client fields."""

    # Ensure required fields are not empty or whitespace
    if not name or not name.strip():
        return False, "Name is required."
    if not addr1 or not addr1.strip():
        return False, "Address Line 1 is required."
    if not city or not city.strip():
        return False, "City is required."
    if not country or not country.strip():
        return False, "Country is required."
    if not phone or not phone.strip():
        return False, "Phone is required."

    return True, ""


def get_clients(records: List[Dict]) -> List[Dict]:
    """Return all records where Type is 'Client'."""

    return [record for record in records if record.get("Type") == CLIENT_TYPE]


def update_client(
    records: List[Dict],
    client_id: str,
    updated_data: Dict
) -> bool:
    """Update a client record by ID."""

    for record in records:
        if record.get("ID") == client_id and record.get("Type") == CLIENT_TYPE:
            record.update(updated_data)
            return True

    return False


def delete_client(records: List[Dict], client_id: str) -> bool:
    """Delete a client record by ID."""

    # enumerate() provides both index and record
    # which allows safe removal using pop()
    for i, record in enumerate(records):
        if record.get("ID") == client_id and record.get("Type") == CLIENT_TYPE:
            records.pop(i)
            return True

    return False


def search_clients(records: List[Dict], search_term: str) -> List[Dict]:
    """Search client records by any field (case-insensitive)."""

    results: List[Dict] = []
    search_term = search_term.lower()

    for record in records:
        if record.get("Type") == CLIENT_TYPE:

            # Check every value in the record
            for value in record.values():

                # Convert value to string because some fields
                # (like zip codes or IDs) may not be strings.
                # This ensures the search works for all data types.
                if search_term in str(value).lower():
                    results.append(record)
                    break  # stop once a match is found

    return results
