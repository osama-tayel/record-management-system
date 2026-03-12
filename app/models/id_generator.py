"""
ID generation utilities for record management system.

Provides helper functions to generate unique IDs for client, flight,
and airline records.
"""

from typing import List, Dict, Any


def get_next_id(records: List[Dict[str, Any]], record_type: str) -> int:
    """Generate the next available ID for a given record type.

    Filters records by type, finds the highest existing ID,
    and returns the next sequential ID. Returns 1 if no records
    of the specified type exist.

    Args:
        records: List of all record dictionaries.
        record_type: Type of record (e.g. 'Client', 'Airline', 'Flight').

    Returns:
        Next available ID as an integer (1 if no records of type exist).

    Examples:
        >>> records = [
        ...     {'ID': 1, 'Type': 'Client'},
        ...     {'ID': 2, 'Type': 'Client'},
        ...     {'ID': 101, 'Type': 'Airline'}
        ... ]
        >>> get_next_id(records, 'Client')
        3
        >>> get_next_id(records, 'Airline')
        102
        >>> get_next_id(records, 'Flight')
        1
    """
    # Filter records to only those matching the specified type
    matching_records = [
        record for record in records
        if record.get('Type') == record_type
    ]

    # Handle empty list case - return 1 if no records of this type exist
    if not matching_records:
        return 1

    # Extract all IDs from matching records (handle missing ID gracefully)
    existing_ids = [
        record['ID'] for record in matching_records
        if 'ID' in record and isinstance(record['ID'], int)
    ]

    # If no valid IDs found, return 1
    if not existing_ids:
        return 1

    # Return the maximum ID plus 1
    return max(existing_ids) + 1
