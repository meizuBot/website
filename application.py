from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute
import typing
import aiohttp
from config import gist
import json

class CoolStarlette(Starlette):
    def __init__(
        self,
        debug: bool = False,
        routes: typing.Sequence[BaseRoute] = None,
        middleware: typing.Sequence[Middleware] = None,
        exception_handlers: typing.Dict[typing.Union[int, typing.Type[Exception]], typing.Callable] = None,
        on_startup: typing.Sequence[typing.Callable] = None,
        on_shutdown: typing.Sequence[typing.Callable] = None,
        lifespan: typing.Callable[["Starlette"], typing.AsyncContextManager] = None,
    ) -> None:
        super().__init__(
            debug=debug,
            routes=routes,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan
        )
        self.session = None
        self.data = None
        self.router.on_startup.append(self.startup)
        self.router.on_shutdown.append(self.shutdown)

    async def startup(self):
        self.session = aiohttp.ClientSession()
        url = "https://api.github.com/gists/" + gist.id
        async with self.session.get(url) as resp:
            data = await resp.json()
        content = data["files"]["data.json"]["content"]
        self.data = content

    async def fetch(self, endpoint: str) -> dict:
        ...

    async def shutdown(self):
        await self.session.close()
