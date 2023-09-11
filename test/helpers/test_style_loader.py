# -*- coding: utf-8 -*-
"""Style loader class test module."""
import pytest

from src.helpers.style_loader import StyleLoader


def test_get_qss_from_file() -> None:
    """Loading style from file."""
    assert isinstance(StyleLoader.get_qss_from_file(), str)


def test_get_qss_from_file_with_incorrect_path() -> None:
    """When loading style from file has incorrect path."""
    with pytest.raises(Exception):
        StyleLoader.get_qss_from_file("")
