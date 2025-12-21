import httpx

from src.api.models import ServerTimeResponse


class TimeClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    async def fetch_time(self) -> ServerTimeResponse:
        async with httpx.AsyncClient(base_url=self._base_url) as client:
            response = await client.get("/time")
            response.raise_for_status()
            return ServerTimeResponse.model_validate(response.json())
