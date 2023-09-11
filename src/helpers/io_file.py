# -*- coding: utf-8 -*-
"""Style loader module."""

import os


class IOFile:
    """Contains all files operations."""

    @staticmethod
    def get_real_path_from_relative_path(relative_path: str) -> str:
        """Get absolute path of project and concatenate with provided path."""
        return os.path.realpath(relative_path)

    @staticmethod
    def load_file_content(path: str) -> str:
        """Load text file content from specified file in path."""
        with open(IOFile.get_real_path_from_relative_path(path), "r") as f:
            content = f.read()

        return content
