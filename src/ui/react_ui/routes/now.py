from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/now")
async def now() -> dict[str, str]:
    return {"now": datetime.now(tz=UTC).isoformat()}