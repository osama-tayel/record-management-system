"""Unit tests for the GUI logic model."""
import unittest
from app.gui.client_tab import (
    validate_client,
    create_client)

class TestGuiLogic(unittest.TestCase):
    """Test cases for the GUI logic functions."""

    def test_validate_client_rejects_empty_name(self):
        """Verify that an empty name is rejected."""
        # Call validate_client with empty name
        test_data={
            "Name": "   ",
            "Address Line 1": "Calle Mayor 1",
            "City": "Valencia",
            "Country": "Spain",
            "Phone": "07712345678"
        }
        is_valid, error = validate_client(
            test_data["Name"],
            test_data["Address Line 1"],
            test_data["City"],
            test_data["Country"],
            test_data["Phone"],
        )
        self.assertFalse(is_valid)
        self.assertEqual(error, "Name is required.")

    def test_validate_client_accepts_valid_input(self):
        """Verify that valid input is accepted."""
        # Call validate_client with all valid fields
        valid_test_data={
            "Name": "Maria Garcia",
            "Address Line 1": "Calle Mayor 1",
            "City": "Valencia",
            "Country": "Spain",
            "Phone": "07712345678",
        }
        is_valid, error = validate_client(
            valid_test_data["Name"],
            valid_test_data["Address Line 1"],
            valid_test_data["City"],
            valid_test_data["Country"],
            valid_test_data["Phone"],
        )
        self.assertTrue(is_valid)
        self.assertEqual(error,"")

    def test_create_client_returns_dict(self):
        """Test that create_client returns a dictionary with correct fields and values."""
        client = create_client(
            client_id= 888,
            name= "Johnny Marr",
            addr1= "87 Charles Street",
            addr2= "Bury",
            addr3= "Manchester",
            city= "Manchester",
            state= "Greater Manchester",
            zip_code= "M45 6AB",
            country= "United Kingdom",
            phone= "01619999999"
        )
        expected_client={
            "ID": 888,
            "Type": "Client",
            "Name": "Johnny Marr",
            "Address Line 1": "87 Charles Street",
            "Address Line 2": "Bury",
            "Address Line 3": "Manchester",
            "City": "Manchester",
            "State": "Greater Manchester",
            "Zip Code": "M45 6AB",
            "Country": "United Kingdom",
            "Phone": "01619999999"
        }
        self.assertIsInstance(client, dict)
        self.assertEqual(client, expected_client)
