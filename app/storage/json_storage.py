"""
JSON storage manager for travel agent record management system.

Handles persistence of client, flight, and airline records to the file system.
"""

import json
from datetime import date, datetime
from pathlib import Path
from typing import List, Dict, Any


class StorageManager:
    """
    Manages saving and loading of records to/from JSON file storage.
    
    Handles conversion of datetime objects to ISO format strings for JSON
    serialisation and creates necessary directories on first save.
    """

    def __init__(self, filepath: str = 'data/records.json') -> None:
        """
        Initialise the storage manager with a file path.
        
        Args:
            filepath: Path to the JSON file for storing records.
                     Defaults to 'data/records.json'.
        """
        self.filepath = Path(filepath)

    def load(self) -> List[Dict[str, Any]]:
        """
        Load records from the JSON file.
        
        Returns:
            List of record dictionaries. Returns an empty list if the file
            doesn't exist (e.g. on first run).
        
        Raises:
            json.JSONDecodeError: If the file contains invalid JSON.
            PermissionError: If the file cannot be read due to permissions.
        """
        if not self.filepath.exists():
            return []
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                records = json.load(file)
                return records if isinstance(records, list) else []
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {self.filepath}: {str(e)}",
                e.doc,
                e.pos
            )
        except PermissionError as e:
            raise PermissionError(
                f"Cannot read file {self.filepath}: {str(e)}"
            )

    def save(self, records: List[Dict[str, Any]]) -> None:
        """
        Save records to the JSON file.
        
        Creates the parent directory if it doesn't exist. Converts date/datetime
        objects to ISO format strings before saving.
        
        Args:
            records: List of record dictionaries to save.
        
        Raises:
            TypeError: If records cannot be serialised to JSON.
            PermissionError: If the file cannot be written due to permissions.
            OSError: If directory creation or file writing fails.
        """
        # Create the data directory if it doesn't exist
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert dates to ISO format strings for JSON serialisation
        serialisable_records = self._convert_dates_to_strings(records)
        
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(serialisable_records, file, indent=4, ensure_ascii=False)
        except TypeError as e:
            raise TypeError(f"Cannot serialise records to JSON: {str(e)}")
        except PermissionError as e:
            raise PermissionError(
                f"Cannot write to file {self.filepath}: {str(e)}"
            )

    def _convert_dates_to_strings(
        self,
        records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Convert date/datetime objects to ISO format strings.
        
        Args:
            records: List of record dictionaries that may contain date objects.
        
        Returns:
            New list with dates converted to strings.
        """
        converted_records = []
        
        for record in records:
            converted_record = {}
            for key, value in record.items():
                if isinstance(value, (date, datetime)):
                    # Convert to ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
                    converted_record[key] = value.isoformat()
                else:
                    converted_record[key] = value
            converted_records.append(converted_record)
        
        return converted_records