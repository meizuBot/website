from .application import CoolStarlette
from starlette.responses import Response
from starlette.routing import Route, Mount
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

__all__ = ("app",)

templates = Jinja2Templates(directory="web/templates")
bot_name = "Walrus"


async def index(request: Request) -> Response:
    return templates.TemplateResponse(
        "index.html", context={"request": request, "name": bot_name}
    )


async def not_found(request, exc):
    return templates.TemplateResponse("404.html", context={"request": request})

routes = [
    Route("/", endpoint=index),
    Mount("/static", StaticFiles(directory="web/static")),
]

exceptions = {404: not_found}

app = CoolStarlette(
    debug=False, routes=routes, exception_handlers=exceptions
)
