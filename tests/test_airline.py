"""Unit tests for the Airline model."""

import unittest
from app.models.airline import (
    AIRLINE_TYPE,
    create_airline,
    validate_airline,
    get_airlines,
    update_airline,
    delete_airline,
    search_airlines
)

class TestAirlineModel(unittest.TestCase):
    """Test cases for the airline model functions."""

    def setUp(self):
        """Set up new test data for each test case."""
        self.records = [
            {"ID": 1, "Type": "Airline", "Company Name": "Virgin Airlines"},
            {"ID": 2, "Type": "Airline", "Company Name": "British Airways"},
            {"ID": 3, "Type": "Airline", "Company Name": "Jet2"},
            {"ID": 4, "Type": "Flight", "Company Name": "A32534"}   
        ]

    def test_create_airline_returns_dict(self):
        """Test that create_airline returns a dictionary with correct fields."""

        airline = create_airline(5, "Airlingus")

        # create_airline should return a dictionary with the correct fields
        self.assertIsInstance(airline, dict)
        self.assertEqual(airline.get("ID"), 5)
        self.assertEqual(airline.get("Type"), AIRLINE_TYPE)
        self.assertEqual(airline.get("Company Name"), "Airlingus")

    def test_validate_airline_rejects_empty_name(self):
        """Verify that an empty name is rejected."""
        # Call validate_airline with empty name
        is_valid, error = validate_airline(
            company_name= "   ",
        )
        self.assertFalse(is_valid)
        # Failure message should state that company name is required
        self.assertEqual(error, "Company Name is required.")

        is_valid, error = validate_airline(
            company_name= "",
        )
        # Validation should fail if name is empty
        self.assertFalse(is_valid)
        # Failure message should state that company name is required
        self.assertEqual(error, "Company Name is required.")

    def test_validate_airline_accepts_valid_input(self):
        """Verify that valid input is accepted."""
        # Call validate_airline with all valid fields
        is_valid, error = validate_airline(company_name= "Virgin Airlines")
        self.assertTrue(is_valid)
        self.assertEqual(error,"")

    def test_get_airlines_filters_correctly(self):
        """Verify that get_airlines correctly filters records by type."""
        airlines = get_airlines(self.records)
        self.assertEqual(len(airlines), 3)
        # Verify that get_airlines only returns records of type 'Airline'
        for r in airlines:
            self.assertEqual(r["Type"], AIRLINE_TYPE)

    def test_update_airline(self):
        """Verify that update_airline correctly updates an airline's information."""
        result = update_airline(self.records, 1, {"Company Name": "EasyJet"})
        # Update should return True if the airline was found and updated
        self.assertTrue(result)
        # Verify that the airline's information was updated
        self.assertEqual(self.records[0]["Company Name"], "EasyJet")

    def test_delete_airline(self):
        """Verify that delete_airline correctly deletes an airline by ID."""
        result = delete_airline(self.records, 3)
        self.assertTrue(result)
        # Verify that the airline was removed from the records
        self.assertEqual(len(self.records), 3)
        for record in self.records:
            self.assertNotEqual(record["ID"], 3)

    def test_search_airlines_finds_match(self):
        """Verify that search_airlines correctly finds airlines by name."""
        results = search_airlines(self.records, "Jet2")
        self.assertEqual(len(results), 1)
        # Verify that the correct airline was returned
        self.assertEqual(results[0]["Company Name"], "Jet2")

    def test_search_airlines_case_insensitive(self):
        """Verify that search_airlines searches case-insensitively."""
        results = search_airlines(self.records, "jet2")
        self.assertEqual(len(results), 1)
        # Verify that the correct airlines was returned
        self.assertEqual(results[0]["Company Name"], "Jet2")