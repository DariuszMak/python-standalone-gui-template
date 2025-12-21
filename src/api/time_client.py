from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime

from src.api.models import ServerTimeResponse

logger = logging.getLogger(__name__)


class TimeClient:
    """Mock client to fetch server time asynchronously."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def fetch_time(self) -> ServerTimeResponse:
        """
        Simulate fetching server time.
        Replace this with actual HTTP requests if needed.
        """
        await asyncio.sleep(0.01)  # simulate network delay
        now = datetime.now(UTC)
        logger.debug("Fetched server time: %s", now.isoformat())
        return ServerTimeResponse(datetime=now)
