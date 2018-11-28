
import concurrent.futures
import json

from aiohttp import web
app = web.Application()
import pickledb
db = pickledb.load('db', True)
import pprint
import requests


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


def _fetch_live_metadata(pkg, version):
    response = requests.get(
        NPM_REGISTRY_FMT.format(pkg=pkg, version=version)
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        app.logger.error(str(e))
        return {}
    return response.json()


def _fetch_live_deps(key):
    """[(pkg, version), (pkg, version), ...]"""
    metadata = _fetch_live_metadata(*key)
    dependencies = metadata.get('dependencies', {})
    return [(p, _clean_version(v)) for p, v in dependencies.items()]


def _store_missing_live_deps(missing_deps):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for (pkg_, version_), subdeps in zip(
            missing_deps, executor.map(_fetch_live_deps, missing_deps)
        ):
            db.set(json.dumps((pkg_, version_)), subdeps)


def _fetch_deps(pkg, version, result):
    """Recursively fetch and iterate over the dependencies of a
    given package (of a given version).

    In order accelrate performance, there are 2 mechanisms taking place:

    1) dependencies are stored locally and are fetched when need be, and
    2) when dependencies are not stored locally, HTTP requests are executed
       in parallel.
    """
    stored_deps = _fetch_stored_deps(pkg, version)
    if stored_deps is not None:
        deps = stored_deps
    else:
        deps = _fetch_live_deps((pkg, version))
        db.set(json.dumps((pkg, version)), deps)

    _store_missing_live_deps(
        [dep for dep in deps if (not db.exists(json.dumps(dep)))]
    )
    for (pkg_, version_) in deps:
        # recursion step
        version_ = _clean_version(version_)
        sub_subdeps = {}
        result[(pkg_, version_)] = sub_subdeps
        _fetch_deps(pkg_, version_, sub_subdeps)


def main(request):
    pkg = request.match_info.get('pkg')
    version = _clean_version(request.match_info.get('version'))

    sub_deps = {}
    result = {(pkg, version): sub_deps}
    _fetch_deps(pkg, version, sub_deps)
    return web.Response(text=pprint.pformat(result))


if __name__ == '__main__':
    app.add_routes([web.get('/{pkg}/{version}', main)])
    web.run_app(app)
