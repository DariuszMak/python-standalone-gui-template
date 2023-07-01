# -*- coding: utf-8 -*-
"""Style loader class test module."""

from app.helpers.style_loader import StyleLoader


def test_get_qss_from_file() -> None:
    """Getting real path test."""
    assert isinstance(StyleLoader.get_qss_from_file(), str)
