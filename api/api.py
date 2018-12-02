
import asyncio
from aiohttp import web
app = web.Application()

from dal.cache_client import cache
from dep_tree import DepTree


def on_get(request):
    pkg = request.match_info.get('pkg')
    version = request.match_info.get('version')
    dt = DepTree(pkg, version)

    cached_result = cache.get(dt.json_key)
    if cached_result is not None:
        return web.json_response(cached_result)

    dt.populate()
    cache.insert(dt.json_key, dt.tree)
    return web.json_response(dt.tree)


if __name__ == '__main__':
    app.add_routes(
        [web.get('/api/{pkg}/{version}', on_get),
         web.get('/api/ping', lambda _: web.json_response('pong'))]
    )
    web.run_app(app)
