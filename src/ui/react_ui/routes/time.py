from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/time")
async def time() -> dict[str, str]:
    return {"datetime": datetime.now(tz=UTC).isoformat()}