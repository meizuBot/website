from .application import CoolStarlette
from starlette.responses import Response, RedirectResponse
from starlette.routing import Route, Mount
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from pprint import pprint

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

    html = ""
    redone = {}


    def gen_list(cmd):
        data = {}
        for l in cmd["subcommands"].values():
            data[l["qualified_name"]] = l
            data.update(gen_list(l))
            
            del data[l["qualified_name"]]["subcommands"]
        return data


    for name, cog in cogs.items():
        data = {"description": cog["description"], "commands": {}}
        for cmd in cog["commands"].values():

            data["commands"][cmd["name"]] = cmd
            data["commands"].update(gen_list(cmd))

            del data["commands"][cmd["name"]]["subcommands"]
        
        redone[name] = data

    def gen_command_html(cmd):
        gen = f"<h3>{cmd['qualified_name']}</h3>\n"

        if desc := cmd["description"]:
            gen += desc

        attrs = []
        if (aliases := cmd["aliases"]) != []:
            custom = aliases
            if (parent := cmd["parent_name"]) != "":
                custom = [f"{parent} {alias}" for alias in aliases]
            attrs.append(f"Aliases: <code>{', '.join(custom)}</code>")
        else:
            attrs.append("Aliases: This commands has no aliases")

        attrs.append(f"Usage: <code>{cmd['qualified_name']} {cmd['signature'].replace('<', '&lt;').replace('>', '&gt;')}</code>")
        attrs.append(f"Returns: {cmd['returns']}")


        gen += "<p>" + "<br>".join(attrs) + "</p>\n"

        if (examples_ := cmd["examples"]) != []:
            examples = "<br>".join(f"<code>{cmd['qualified_name']}</code> <code>{example}</code>" for example in examples_)
        else:
            examples = f"<code>{cmd['qualified_name']}</code>"
        
        if isinstance((params_ := cmd["params"]), dict):
            params = "<br>".join(f"<code>{param}</code>: {value}" for param, value in params_.items())
        else:
            params = params_

        gen += f'<h4>Examples</h4><p>{examples}</p>'
        gen += f'\n<h4>Parameters</h4><p>{params}</p>'

        return gen

    for name, cog in redone.items():
        add = f"<h2 name={name}>{name}</h2>\n"
        if (desc := cog["description"]) != "":
            add += f"<p>{desc}</p>\n"

        add += "<hr>\n\n"

        for command in cog["commands"].values():
            add += gen_command_html(command) + "<hr>\n\n"

        html += add

    return templates.TemplateResponse("commands.html", context={"request": request, "cogs": cogs, "test": html})

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
