
import asyncio
from aiohttp import web

from dal.cache_client import cache
from dep_view import fetch_deps


async def on_get(request):
    pkg = request.match_info.get('pkg')
    version = request.match_info.get('version')

    cached_result = cache.get(pkg, version)
    if cached_result is not None:
        return web.json_response(cached_result)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, fetch_deps, pkg, version)
    cache.insert(pkg, version, result)
    return web.json_response(result)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(
        [web.get('/api/{pkg}/{version}', on_get),
         web.get('/api/ping', lambda _: web.json_response('pong'))]
    )
    web.run_app(app)
