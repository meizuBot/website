from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route, Mount
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from . import ipc

__all__ = ("app",)

templates = Jinja2Templates(directory="web/templates")
client = ipc.Client()

bot_name = "Walrus"


async def start():
    await client.initiate()


async def stop():
    await client.close()


async def index(request: Request) -> Response:
    #stats = await client.request("stats")
    return templates.TemplateResponse(
        "bootstrap_index.html", context={"request": request, "name": bot_name}
    )


async def not_found(request, exc):
    return templates.TemplateResponse("404.jinja", context={"request": request})


async def stats(request):
    return templates.TemplateResponse("stats.jinja", context={"request": request, "name": bot_name})

async def test(request: Request) -> Response:
    return templates.TemplateResponse(
        "base.html", context={"request": request}
    )

async def test2(request):
    return templates.TemplateResponse(
        "newindex.html", context={"request": request}
    )

async def bootstrap(r):
    return templates.TemplateResponse(
        "bootstrap.html", context={"request": r}
    )


routes = [
    Route("/", endpoint=index),
    Route("/test", endpoint=test),
    Route("/t", endpoint=test2),
    Route("/b", endpoint=bootstrap),
    Route("/stats", endpoint=stats),
    Mount("/static", StaticFiles(directory="web/static")),
]

exceptions = {404: not_found}

app = Starlette(
    debug=False, routes=routes, exception_handlers=exceptions, on_startup=[start], on_shutdown=[stop]
)
