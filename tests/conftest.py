import asyncio

from _pytest.main import Session


def pytest_sessionstart(_session: Session) -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.new_event_loop()
