from datetime import UTC, datetime

from litestar import get


@get("/api/now")
async def now() -> dict[str, str]:
    return {"now": datetime.now(tz=UTC).isoformat()}
