# -*- coding: utf-8 -*-
"""Style loader class test module."""
from app.helpers.style_loader import StyleLoader


def test_get_real_path_from_relative_path() -> None:
    """Getting real path test."""
    ugly_format = "app/ui/themes\\main_theme.qss"
    assert (
        StyleLoader.get_real_path_from_relative_path(ugly_format)
        == "D:\\Repos\\python-standalone-gui-template\\test\\app\\ui\\themes\\main_theme.qss"
    )
