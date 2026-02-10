from datetime import datetime, timezone
from litestar import get

@get("/api/now")
async def now() -> dict:
    return {
        "now": datetime.now(tz=timezone.utc).isoformat()
    }
