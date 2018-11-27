
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


def _fetch_deps(pkg, version, result):
    stored_deps = _fetch_stored_deps(pkg, version)
    if stored_deps is not None:
        deps = stored_deps
    else:
        deps = _fetch_live_deps((pkg, version))
        db.set(json.dumps((pkg, version)), deps)

    all_deps = {(p, v) for p, v in deps}

    cached_deps = {(p, v) for p, v in deps if db.exists(json.dumps((p, v)))}
    cached_deps_subdeps = {(p, v): db.get((p, v)) for p, v in cached_deps}

    missing_deps = all_deps.difference(cached_deps)
    missing_deps_subdeps = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for (pkg_, version_), subdeps in zip(
                missing_deps, executor.map(_fetch_live_deps, missing_deps)
            ):
            missing_deps_subdeps[
                (pkg_, _clean_version(version_))
            ] = subdeps

    all_deps_subdeps = {**missing_deps_subdeps, **cached_deps_subdeps}
    for (pkg_, version_), subdeps in all_deps_subdeps.items():
        version_ = _clean_version(version_)
        sub_sub_deps = {}
        result[(pkg_, version_)] = sub_sub_deps
        _fetch_deps(pkg_, version_, sub_sub_deps)


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
