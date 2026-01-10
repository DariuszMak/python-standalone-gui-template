from datetime import UTC, datetime
import httpx
from litestar import get
import logging

logger = logging.getLogger(__name__)

TIME_API_URLS = [
    "https://gettimeapi.dev/v1/time?timezone=UTC",
    "https://aisenseapi.com/services/v1/datetime",
]


@get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


@get("/time")
async def current_time() -> dict[str, str]:
    async with httpx.AsyncClient(timeout=2.0) as client:
        for url in TIME_API_URLS:
            try:
                logger.info("Gathering time from Internet: %s", url)
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                datetime_str = (
                     data.get("iso8601")    
                    or data.get("datetime")        
                )
                if datetime_str:
                    logger.info("Got time from Internet: %s", datetime_str)
                    return {"datetime": datetime_str}
            except httpx.HTTPError as exc:
                logger.warning(
                    "Failed to fetch time from Internet (%s), trying next source",
                    exc.__class__.__name__,
                )
                continue

    local_time = datetime.now(UTC).isoformat()
    logger.warning("All remote sources failed, returning local UTC: %s", local_time)
    return {"datetime": local_time}
