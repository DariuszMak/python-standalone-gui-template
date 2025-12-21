from __future__ import annotations

import logging
from datetime import datetime

import httpx

from src.api.models import ServerTimeResponse

logger = logging.getLogger(__name__)


class TimeClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def fetch_time(self) -> ServerTimeResponse:
        url = f"{self.base_url}/time"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        payload = response.json()
        server_time = datetime.fromisoformat(payload["datetime"])

        logger.debug("Fetched server time: %s", server_time.isoformat())

        return ServerTimeResponse(datetime=server_time)
