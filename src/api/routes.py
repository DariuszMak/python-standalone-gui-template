from datetime import UTC, datetime

from litestar import get


@get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


@get("/time")
async def current_time() -> dict[str, str]:
    return {"datetime": datetime.now(UTC).isoformat()}
