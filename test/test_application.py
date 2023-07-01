# -*- coding: utf-8 -*-
"""Unit tests module."""
from app import application


def test_app_hello_world() -> None:
    """Hello world test."""
    assert application.hello_world() == "Hello World!"
