
import asyncio
from aiohttp import web
app = web.Application()

from dal.cache_client import cache
from dep_tree import DepTree


async def on_get(request):
    pkg = request.match_info.get('pkg')
    version = request.match_info.get('version')

    dt = DepTree(pkg, version)
    cached_result = cache.get(pkg, dt.version)
    if cached_result is not None:
        return web.json_response(cached_result)
    result = {dt.json_key: await dt.populate()}
    cache.insert(pkg, dt.version, result)
    return web.json_response(result)


if __name__ == '__main__':
    app.add_routes(
        [web.get('/api/{pkg}/{version}', on_get),
         web.get('/api/ping', lambda _: web.json_response('pong'))]
    )
    web.run_app(app)
