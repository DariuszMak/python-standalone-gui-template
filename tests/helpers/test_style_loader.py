import pytest

from src.helpers.style_loader import StyleLoader


def test_get_qss_from_file() -> None:
    assert isinstance(StyleLoader.get_qss_from_file(), str)


def test_get_qss_from_file_with_incorrect_path() -> None:
    with pytest.raises((PermissionError, IsADirectoryError)):
        StyleLoader.get_qss_from_file("")
