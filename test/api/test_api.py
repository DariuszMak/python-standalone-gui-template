from litestar import Litestar
from litestar.testing import TestClient

from src.api.routes import ping  # replace 'your_module' with the actual filename if needed (without .py)

app = Litestar(route_handlers=[ping])


def test_ping_route():
    with TestClient(app) as client:
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}
