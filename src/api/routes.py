import logging
from datetime import datetime
from pathlib import Path

import httpx
from fastapi import APIRouter
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter()

TIME_API_URLS = [
    "https://gettimeapi.dev/v1/time?timezone=UTC",
    "https://aisenseapi.com/services/v1/datetime",
]


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(Path("src/ui/pyside_ui/forms/icons/images/program_icon.ico"))


@router.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


@router.get("/time")
async def current_time() -> dict[str, str]:
    async with httpx.AsyncClient(timeout=2.0) as client:
        for url in TIME_API_URLS:
            try:
                logger.info("Gathering time from Internet: %s", url)
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                datetime_str = data.get("iso8601") or data.get("datetime")
                if datetime_str:
                    dt = datetime.fromisoformat(datetime_str).astimezone()
                    return {"datetime": dt.isoformat()}
            except httpx.HTTPError:
                continue
    return {"datetime": datetime.now().astimezone().isoformat()}
