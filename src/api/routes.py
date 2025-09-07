from litestar import get


@get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}
