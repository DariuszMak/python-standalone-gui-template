import os
import sys


class IOFile:
    @staticmethod
    def get_real_path_from_relative_path(relative_path: str) -> str:
        base_path = None

        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.realpath(os.path.join(base_path, relative_path))

    @staticmethod
    def load_file_content(path: str) -> str:
        with open(IOFile.get_real_path_from_relative_path(path)) as f:
            content = f.read()

        return content
