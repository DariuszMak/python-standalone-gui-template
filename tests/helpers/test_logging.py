import logging

import pytest

from src.helpers.logging_setup import logging_setup


@pytest.fixture(autouse=True)
def reset_logging():
    logger = logging.getLogger()
    logger.handlers.clear()
    yield
    logger.handlers.clear()


def test_logging_setup_adds_handlers(tmp_path):
    log_file = tmp_path / "test.log"

    logging_setup(log_file=str(log_file))

    logger = logging.getLogger()
    handler_types = {type(h) for h in logger.handlers}

    assert logging.StreamHandler in handler_types
    assert logging.FileHandler in handler_types


def test_logging_writes_to_file(tmp_path):
    log_file = tmp_path / "test.log"

    logging_setup(log_file=str(log_file))

    logger = logging.getLogger()
    logger.info("test message")

    with open(log_file) as f:
        content = f.read()

    assert "test message" in content


def test_logging_level(tmp_path):
    log_file = tmp_path / "test.log"

    logging_setup(level=logging.DEBUG, log_file=str(log_file))

    logger = logging.getLogger()

    assert logger.level == logging.DEBUG


def test_formatter_is_set(tmp_path):
    log_file = tmp_path / "test.log"

    logging_setup(log_file=str(log_file))

    logger = logging.getLogger()

    for handler in logger.handlers:
        assert handler.formatter is not None


def test_no_duplicate_handlers(tmp_path):
    log_file = tmp_path / "test.log"

    logging_setup(log_file=str(log_file))
    logging_setup(log_file=str(log_file))

    logger = logging.getLogger()

    assert len(logger.handlers) == 2
