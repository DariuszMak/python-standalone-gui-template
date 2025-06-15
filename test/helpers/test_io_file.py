"""Style loader class test module."""

import os

from src.helpers.io_file import IOFile  # Import the class that contains the method


def test_get_real_path_from_relative_path() -> None:
    # Create an instance of IOFile
    your_instance = IOFile()

    # Define a relative path and expected result
    relative_path = os.path.normpath("example_folder/example_file.txt")
    expected_result = os.path.realpath(os.path.join(os.path.abspath("."), relative_path))

    # Call the method and check if it returns the expected result
    result = your_instance.get_real_path_from_relative_path(relative_path)
    assert result == expected_result

    # Test with an absolute path, it should return the same path
    absolute_path = os.path.normpath("/absolute/path/to/some/file.txt")
    drive, path = os.path.splitdrive(your_instance.get_real_path_from_relative_path(absolute_path))
    assert path == absolute_path

    # Test with a different relative path, adjust the expected result accordingly
    different_relative_path = os.path.normpath("another_folder/another_file.txt")
    different_expected_result = os.path.realpath(os.path.join(os.path.abspath("."), different_relative_path))
    assert your_instance.get_real_path_from_relative_path(different_relative_path) == different_expected_result
