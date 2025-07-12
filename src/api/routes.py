from litestar import get


@get("/ping")
def ping() -> dict:
    return {"message": "pong"}
