import asyncio

from _pytest.main import Session


def pytest_sessionstart(session: Session) -> None:  # noqa: ARG001
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.new_event_loop()
