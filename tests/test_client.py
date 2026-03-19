"""Unit tests for the Client model."""

import unittest
from app.models.client import (
    CLIENT_TYPE,
    create_client,
    validate_client,
    get_clients,
    update_client,
    delete_client,
    search_clients
)

class TestClientModel(unittest.TestCase):
    """Test cases for the client model functions."""

    def setUp(self):
        """Set up new test data for each test case."""
        self.test_client_a = create_client(
            client_id= 433,
            name= "Johnny Marr",
            addr1= "87 Charles Street",
            addr2= "Bury",
            addr3= "",
            city= "Manchester",
            state= " Greater Manchester",
            zip_code= "M45 999",
            country= "United Kingdom",
            phone= "01619999999",
        )
        self.test_client_b = create_client(
            client_id= 434,
            name= "Steven Morrissey",
            addr1= "21 First Avenue",
            addr2= "",
            addr3="",
            city= "London",
            state= " Greater London",
            zip_code= "SW1A 1AA",
            country= "United Kingdom",
            phone= "0161888888",
        )
        self.non_client_record = {
            "ID": 777,
            "Type": "Flight",
            "Name": "John Smith"
        }
        self.records = [self.test_client_a, self.test_client_b, self.non_client_record]

    def test_create_client_returns_dict(self):
        """Test that create_client returns a dictionary with correct fields and values."""
        client = create_client(
            client_id= 999,
            name= "Bob Jones",
            addr1= "32 High Road",
            addr2= "Sale",
            addr3= "Manchester",
            city= "Manchester",
            state= " Greater Manchester",
            zip_code= "M47 123",
            country= "United Kingdom",
            phone= "01619999998"
        )
        expected_client = {
            "ID": 999,
            "Type": CLIENT_TYPE,
            "Name": "Bob Jones",
            "Address Line 1": "32 High Road",
            "Address Line 2": "Sale",
            "Address Line 3": "Manchester",
            "City": "Manchester",
            "State": " Greater Manchester",
            "Zip Code": "M47 123",
            "Country": "United Kingdom",
            "Phone Number": "01619999998"
        }
        # create_client should return a dictionary with the correct fields and values
        self.assertIsInstance(client, dict)
        self.assertEqual(client, expected_client)

    def test_validate_client_rejects_empty_name(self):
        """Validate that an empty name is rejected."""
        # Call validate_client with empty name
        is_valid, error = validate_client(
            name= "   ",
            addr1= "32 High Road",
            city= "Manchester",
            country= "United Kingdom",
            phone= "01619999998",
        )
        # Failure message should state that name is required
        self.assertFalse(is_valid)
        self.assertEqual(error, "Name is required.")

        is_valid, error = validate_client(
            name= "",
            addr1= "32 High Road",
            city= "Manchester",
            country= "United Kingdom",
            phone= "01619999998",
        )
        # Failure message should state that name is required
        self.assertFalse(is_valid)
        self.assertEqual(error, "Name is required.")

    def test_validate_client_accepts_valid_input(self):
        """Validate that valid input is accepted."""
        # Call validate_client with all valid fields
        is_valid, error = validate_client(
            name= "Bob Jones",
            addr1= "32 High Road",
            city= "Manchester",
            country= "United Kingdom",
            phone= "01619999998",
        )
        self.assertTrue(is_valid)
        self.assertEqual(error,"")

    def test_get_clients_filters_correctly(self):
        """Test that get_clients correctly filters records by type."""
        clients = get_clients(self.records)
        self.assertEqual(len(clients), 2)
        # Verify that all returned records are of type 'Client'
        for c in clients:
            self.assertEqual(c["Type"], CLIENT_TYPE)

    def test_update_client(self):
        """Test that update_client correctly updates a client's information."""
        updated_data = {"City": "Madrid", "Country": "Spain"}
        result = update_client(self.records, 433, updated_data)
        # Update should return True if the client was found and updated
        self.assertTrue(result)
        # Verify that the client's information was updated
        self.assertEqual(self.records[0]["City"], "Madrid")
        self.assertEqual(self.records[0]["Country"], "Spain")

    def test_delete_client(self):
        """Test that delete_client correctly deletes a client by ID."""
        result = delete_client(self.records, 434)
        # Delete should return True if the client was found and deleted
        self.assertTrue(result)
        # Verify that the client was removed from the records
        self.assertEqual(len(self.records), 2)
        for record in self.records:
            self.assertNotEqual(record["ID"], 434)

    def test_search_clients_finds_match(self):
        """Test that search_clients finds the correct clients by name."""
        results = search_clients(self.records, "Johnny")
        self.assertEqual(len(results), 1)
        # Verify that the correct client was returned
        self.assertEqual(results[0]["Name"], "Johnny Marr")

    def test_search_clients_case_insensitive(self):
        """Test that search_clients searches case-insensitively."""
        results = search_clients(self.records, "johnny")
        self.assertEqual(len(results), 1)
        # Verify that the correct client was returned
        self.assertEqual(results[0]["Name"], "Johnny Marr")
