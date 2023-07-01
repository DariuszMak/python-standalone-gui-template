# -*- coding: utf-8 -*-
"""Style loader class test module."""
import os

from app.helpers.style_loader import StyleLoader


def test_get_qss_from_file() -> None:
    """Getting real path test."""
    assert isinstance(StyleLoader.get_qss_from_file(os.path.join("app", "ui", "themes", "main_theme.qss")), str)
