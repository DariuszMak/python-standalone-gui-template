import asyncio

from _pytest.main import Session


def pytest_sessionstart(session: Session) -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.new_event_loop()
