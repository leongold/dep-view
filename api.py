
import asyncio
from aiohttp import web

from dep_view import fetch_deps


async def on_get(request):
    pkg = request.match_info.get('pkg')
    version = request.match_info.get('version')
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, fetch_deps, pkg, version)
    return web.json_response(result)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(
        [web.get('/{pkg}/{version}', on_get),
         web.get('/ping', lambda _: web.json_response('pong'))]
    )
    web.run_app(app, port=8081)
