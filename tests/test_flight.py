"""Unit tests for the Flight model."""

import unittest
from app.models.flight import (
    FLIGHT_TYPE,
    create_flight,
    validate_flight,
    get_flights,
    update_flight,
    delete_flight,
    search_flights,
)

class TestFlightModel(unittest.TestCase):
    """Test cases for the flight model functions."""

    def setUp(self):
        """Setup flight data for test cases."""""
        self.flight=create_flight(
            flight_id=222,
            client_id=333,
            airline_id=444,
            flight_date="2026-06-05",
            start_city="Manchester",
            end_city="Paris"
        )
        flight_two=create_flight(
            flight_id=555,
            client_id=666,
            airline_id=777,
            flight_date="2026-01-02",
            start_city="Madrid",
            end_city="Lisbon"
        )
        # Create a non-flight record to test filtering in get_flights
        self.records=[self.flight, flight_two,
        {" ID": 888, "Type": "client", "Name": "Johnny Marr"}
        ]

    def test_create_flight_returns_dict(self):
        """Test that create_flight returns a dictionary with correct fields and values."""
        self.assertIsInstance(self.flight, dict)
        self.assertEqual(self.flight.get("ID"), 222)
        self.assertEqual(self.flight.get("Type"), "Flight")
        self.assertEqual(self.flight.get("Client_ID"), 333)
        self.assertEqual(self.flight.get("Airline_ID"), 444)
        self.assertEqual(self.flight.get("Date"), "2026-06-05")
        self.assertEqual(self.flight.get("Start City"), "Manchester")
        self.assertEqual(self.flight.get("End City"), "Paris")

    def test_validate_flight_rejects_invalid_date(self):
        """Verify that invalid date formats are rejected."""
        # Call validate_flight with invalid date format
        is_valid, error = validate_flight(
            client_id=333,
            airline_id=444,
            flight_date="6th May 2026",
            start_city="Manchester",
            end_city="Paris"
        )
        self.assertFalse(is_valid)
        # Failure message should state that date must be in ISO format
        self.assertEqual(error, "Date must be in ISO format YYYY-MM-DD.")

    def test_validate_flight_accepts_valid_date(self):
        """Verify that valid date is accepted."""
        # Call validate_flight with all valid fields
        is_valid, error = validate_flight(
            client_id=333,
            airline_id=444,
            flight_date="2026-06-05",
            start_city="Manchester",
            end_city="Paris"
        )
        self.assertTrue(is_valid)
        self.assertEqual(error,"")

    def test_validate_flight_rejects_non_integer_ids(self):
        """Verify that non-integer IDs are rejected."""
        # Call validate_flight with non-integer client_id
        is_valid, error = validate_flight(
            client_id="333",
            airline_id=444,
            flight_date="2026-06-05",
            start_city="Manchester",
            end_city="Paris"
        )
        self.assertFalse(is_valid)
        # Failure message should state that Client_ID must be an integer
        self.assertEqual(error, "Client_ID must be an integer.")

        # Call validate_flight with non-integer airline_id
        is_valid, error = validate_flight(
            client_id=333,
            airline_id=444.1,
            flight_date="2026-06-05",
            start_city="Manchester",
            end_city="Paris"
        )
        self.assertFalse(is_valid)
        # Failure message should state that Airline_ID must be an integer
        self.assertEqual(error, "Airline_ID must be an integer.")

    def test_get_flights_filters_correctly(self):
        """Verify that get_flights correctly filters records by type."""
        flights = get_flights(self.records)
        self.assertEqual(len(flights), 2)
        # Verify that get_flights only returns records of type 'Flight'
        for r in flights:
            self.assertEqual(r["Type"], FLIGHT_TYPE)

    def test_update_flight(self):
        """Verify that update_flight correctly updates a flight record."""
        updated_data = {
            "Start City": "Los Angeles",
            "End City": "Dublin"
        }
        result = update_flight(self.records, flight_id=222, updated_data=updated_data)
        self.assertTrue(result)
        # Verify that the flight record was updated
        for record in self.records:
            if record.get("ID") == 222 and record.get("Type") == FLIGHT_TYPE:
                self.assertEqual(record.get("Start City"), "Los Angeles")
                self.assertEqual(record.get("End City"), "Dublin")

    def test_delete_flight(self):
        """Verify that delete_flight correctly deletes a flight record."""
        result = delete_flight(self.records, flight_id=222)
        self.assertTrue(result)
        # Verify that the flight record was deleted
        for record in self.records:
            self.assertFalse(record.get("ID") == 222 and record.get("Type") == FLIGHT_TYPE)

    def test_search_flights_finds_match(self):
        """Verify that search_flights correctly finds flights by start city."""
        results = search_flights(self.records, "Madrid")
        self.assertEqual(len(results), 1)
        # Verify that the correct flight was returned
        self.assertEqual(results[0]["Start City"], "Madrid")
