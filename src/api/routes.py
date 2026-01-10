from datetime import UTC, datetime

from datetime import UTC, datetime

import httpx
from litestar import get

from litestar import get

TIME_API_URL = "https://worldtimeapi.org/api/timezone/Etc/UTC"

@get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}






@get("/time")
async def current_time() -> dict[str, str]:
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(TIME_API_URL)
            resp.raise_for_status()
            data = resp.json()

            return {"datetime": data["datetime"]}
    except Exception:
        return {"datetime": datetime.now(UTC).isoformat()}
