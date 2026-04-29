from typing import Any

import httpx

from src.helpers.config.config import Config


async def fetch_time() -> str:

    config = Config()

    async with httpx.AsyncClient(timeout=2.0) as client:
        resp = await client.get(f"{config.api_base_url}/time")
        resp.raise_for_status()
        data: Any = resp.json()
        return str(data["datetime"])
