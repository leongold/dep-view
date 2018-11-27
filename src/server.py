
import asyncio
import json

from aiohttp import web
import pickledb
import requests
db = pickledb.load('db', True)


NPM_REGISTRY_FMT = 'https://registry.npmjs.org/{pkg}/{version}'


def _clean_version(version):
    v = version.replace('~', '')
    if '>' in v:
        v = v[v.find(' '):]
    if '<' in v:
        v = v[:v.find( '')]
    return v


def _fetch_stored_deps(pkg, version):
    """[(pkg, version), (pkg, version), ...]"""
    key = json.dumps((pkg, version))
    if db.exists(key):
        # db.get has no fallback value
        return db.get(key)
    return None


async def _fetch_live_metadata(pkg, version):
    response = requests.get(
        NPM_REGISTRY_FMT.format(pkg=pkg, version=version)
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        app.logger.error(str(e))
        return {}
    return response.json()


async def _fetch_live_deps(pkg, version):
    """[(pkg, version), (pkg, version), ...]"""
    metadata = await _fetch_live_metadata(pkg, version)
    dependencies = metadata.get('dependencies', {})
    return [(p, v.replace('~', '')) for p, v in dependencies.items()]


async def _fetch_deps(pkg, version, result):
    version = _clean_version(version)
    stored_deps = _fetch_stored_deps(pkg, version)
    if stored_deps is not None:
        deps = stored_deps
    else:
        deps = await _fetch_live_deps(pkg, version)
        db.set(json.dumps((pkg, version)), deps)

    result_ = {}
    for pkg_, version_ in deps:
        await _fetch_deps(pkg_, version_, result_)
    result[json.dumps((pkg, version))] = result_


async def main(request):
    pkg = request.match_info.get('pkg')
    version = request.match_info.get('version')
    result = {}
    await _fetch_deps(pkg, version, result)
    return web.json_response(result)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/{pkg}/{version}', main)])
    web.run_app(app)
