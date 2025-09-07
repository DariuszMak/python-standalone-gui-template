from litestar import get


@get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}
