from datetime import UTC, datetime

from litestar import get


@get("/api/now")
async def now() -> dict:
    return {"now": datetime.now(tz=UTC).isoformat()}
