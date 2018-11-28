
import requests
import concurrent.futures
import json

from aiohttp import web
app = web.Application()

from dep_view import fetch_deps


def on_get(request):
    pkg = request.match_info.get('pkg')
    version = request.match_info.get('version')
    return web.json_response(fetch_deps(pkg, version))


if __name__ == '__main__':
    app.add_routes(
        [web.get('/{pkg}/{version}', on_get),
         web.get('/ping', lambda _: web.json_response('pong'))]
    )
    web.run_app(app)
