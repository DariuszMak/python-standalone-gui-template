from datetime import datetime
from pathlib import Path

import httpx
import structlog
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse

logger = structlog.get_logger(__name__)
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
            log = logger.bind(url=url)
            try:
                log.info("fetching_external_time")
                resp = await client.get(url)
                resp.raise_for_status()

                data = resp.json()
                datetime_str = data.get("iso8601") or data.get("datetime")

                if datetime_str:
                    dt = datetime.fromisoformat(datetime_str).astimezone()
                    log.info("external_time_received", timestamp=dt.isoformat())
                    return {"datetime": dt.isoformat()}

            except httpx.HTTPError as e:
                log.warning("time_api_request_failed", error=str(e))
                continue

    local_dt = datetime.now().astimezone().isoformat()
    logger.info("falling_back_to_local_time", timestamp=local_dt)
    return {"datetime": local_dt}


@router.get("/{full_path:path}", include_in_schema=False)
async def ignore_noise(full_path: str) -> Response:
    if full_path.startswith(".well-known") or full_path.endswith(".map"):
        return Response(status_code=204)

    logger.debug("unhandled_path_requested", path=full_path)
    return Response(status_code=404)
