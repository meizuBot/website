from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute
import typing
import aiohttp
from config import gist

def filter_subcommands(command, subcommands):
    ...

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
        try:
            raise aiohttp.ClientConnectorError
        except aiohttp.ClientConnectorError:
            ...
        if endpoint == "/all":
            return self.data
        
        if endpoint in ("/stats", "/socket", "/cogs"):
            return self.data[endpoint]
        
        if endpoint.startswith("/cog/"):
            cog = endpoint.lstrip("/cog/")
            return self.data["cogs"].get(cog)
        
        if endpoint.startswith("/command/"):
            command = endpoint.lstrip("/command/")
            for cog in self.data["cogs"]:
                for cmd in cog["commands"]:
                    if command == cmd:
                        return cmd
                    for subcmd in cmd["subcommands"]:
                        if command == cmd:
                            return cmd
        

    async def shutdown(self):
        await self.session.close()
