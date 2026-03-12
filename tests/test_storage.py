""" Unit tests for the StorageManager class in json_storage.py."""
import unittest
import os
import tempfile
import shutil
from app.storage.json_storage import StorageManager

class TestStorageManager(unittest.TestCase):
    """
    Unit tests for the TestStorageManager class.

    Verifies that StorageManager correctly saves records to a JSON file,
    loads them back, and handles edge cases such as missing files and
    empty datasets. All tests use a temporary file to ensure isolation
    from real application data.
    """
    def setUp(self):
        """ 
        Create a temporary directory and file for each test case,
        to ensure isolation from the real data.
        """
        # Creates a unique temporary directory for this test run.
        self.temp_dir = tempfile.mkdtemp()
        # Create file path within the temp directory.
        self.temp_file = os.path.join(self.temp_dir, "test_file.json")
        # Initialise StorageManager with the temp file path.
        self.storage = StorageManager(self.temp_file)

    def tearDown(self):
        """
        Remove the directory and components after each test case,
        to ensure no test data remains.
        """
        # Remove the temporary directory and all content.
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_non_existent_file(self):
        """
        Verify that loading from a non-existent JSON file returns an empty list.

        This establishes the expected behaviour for first-run scenarios where no
        storage file has been created yet, and ensures load() handles missing files
        gracefully without raising exceptions.
        """
        # Load() should return an empty list ([]) instead of raising an error.
        result = self.storage.load()
        self.assertEqual(result, [])


    def test_save_and_load_round_trip(self):
        """
        Ensure that data saved to the JSON file can be loaded back unchanged.

        This confirms that StorageManager correctly serialises and deserialises
        records, preserving structure, field names, and values across the full
        save/load cycle.
        """
        # Define a test record to save.
        test_data = [
            {
                "ID": 1,
                "Type": "Flight",
                "Client_ID": 101,
                "Airline_ID": 201,
                "Date": "2026-03-15", 
                "Start City": "London",
                "End City": "New York"
            }
        ]
        # Save the test data to the JSON file.
        self.storage.save(test_data)
        # Load the data back from the file.
        loaded_data = self.storage.load()
        # The loaded data should match exactly what was saved.
        self.assertEqual(loaded_data, test_data)


    def test_save_creates_file(self):
        """
        Confirm that calling save() results in a JSON file being created on disk.

        This verifies that StorageManager writes to the specified file path and
        does not rely solely on in-memory storage.
        """
        # Save the test data to trigger a file creation.
        self.storage.save([{"id": 1, "Company Name": "British Airways"}])
        # The file should exist after save() is called.
        self.assertTrue(os.path.exists(self.temp_file))

    def test_save_empty_list(self):
        """
        Confirm that saving an empty list does not raise an exception.

        This validates that StorageManager can produce a valid JSON file 
        for an empty dataset.
        """
        # Attempt to save an empty list
        self.storage.save([])

        # Load the file back
        new_file = self.storage.load()
        # The loaded data should be an empty list
        self.assertEqual(new_file, [])
