
import logging

from aiohttp import web

from dep_tree import DepTree


def on_get(request):
    try:
        pkg = request.match_info.get('pkg')
        version = request.match_info.get('version')
        dt = DepTree(pkg, version)
        dt.populate()
        return web.json_response(dt.tree)
    except Exception as e:
        logging.error(str(e))
        return web.HTTPInternalServerError()


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(
        [web.get('/api/{pkg}/{version}', on_get),
         web.get('/api/ping', lambda _: web.json_response('pong'))]
    )
    web.run_app(app)
