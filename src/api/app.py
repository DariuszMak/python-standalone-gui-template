from litestar import Litestar

from src.api.routes import ping

app = Litestar(route_handlers=[ping])
