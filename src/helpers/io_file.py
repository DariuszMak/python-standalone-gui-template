"""Style loader module."""

import os
import sys


class IOFile:
    """Contains all files operations."""

    @staticmethod
    def get_real_path_from_relative_path(relative_path: str) -> str:
        """Get absolute path of project and concatenate with provided path."""
        base_path = None

        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.realpath(os.path.join(base_path, relative_path))

    @staticmethod
    def load_file_content(path: str) -> str:
        """Load text file content from specified file in path."""
        with open(IOFile.get_real_path_from_relative_path(path)) as f:
            content = f.read()

        return content
