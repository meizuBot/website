from .application import CoolStarlette
from starlette.responses import Response, RedirectResponse
from starlette.routing import Route, Mount
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn

__all__ = ("app",)

templates = Jinja2Templates(directory="web/templates")
bot_name = "Walrus"


async def index(request: Request) -> Response:
    return templates.TemplateResponse(
        "index.html", context={"request": request, "name": bot_name}
    )


async def not_found(request, exc):
    return templates.TemplateResponse("404.html", context={"request": request})

async def privacy(request: Request) -> Response:
    return templates.TemplateResponse("privacy.html", context={"request": request})

async def invite(request: Request) -> Response:
    return RedirectResponse("https://google.com")

async def support(request: Request) -> Response:
    return RedirectResponse("https://google.com")

async def commands(request: Request) -> Response:
    cogs = await request.app.fetch("cogs")
    return templates.TemplateResponse("commands.html", context={"request": request, "cogs": cogs})

routes = [
    Route("/", endpoint=index),
    Route("/commands", endpoint=commands),
    Route("/invite", endpoint=invite),
    Route("/support", endpoint=support),
    Route("/privacy", endpoint=privacy),
    Mount("/static", StaticFiles(directory="web/static")),
]

exceptions = {404: not_found}

app = CoolStarlette(
    debug=False, routes=routes, exception_handlers=exceptions
)
