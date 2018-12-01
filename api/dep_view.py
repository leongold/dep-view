
import concurrent.futures
import json

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from dal import to_json_key
from dal import from_json_key
from dal.mongo_client import mongo


NPM_REGISTRY_FMT = 'https://registry.npmjs.org/{pkg}/{version}'


def _clean_version(version):
    v = version.replace('~', '')
    if '>' in v:
        v = v[v.find(' '):]
    if '<' in v:
        v = v[:v.find('')]
    return v


def _fetch_live_metadata(pkg, version):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)

    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(
        NPM_REGISTRY_FMT.format(pkg=pkg, version=version)
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return {}
    return response.json()


def _fetch_live_deps(key):
    """[(pkg, version), (pkg, version), ...]"""
    metadata = _fetch_live_metadata(*key)
    dependencies = metadata.get('dependencies', {})
    return [(p, _clean_version(v)) for p, v in dependencies.items()]


def _store_missing_live_deps(missing_deps):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for (pkg, version), subdeps in zip(
            missing_deps, executor.map(_fetch_live_deps, missing_deps)
        ):
            mongo.insert(pkg, version, subdeps)


def _fetch_deps(pkg, version, result):
    """Recursively fetch and iterate over the dependencies of a
    given package (of a given version).

    In order accelrate performance, there are 2 mechanisms taking place:

    1) dependencies are stored locally and are fetched when need be, and
    2) when dependencies are not stored locally, HTTP requests are executed
       in parallel.
    """
    stored_deps = mongo.get(pkg, version)
    if stored_deps is not None:
        deps = stored_deps
    else:
        deps = _fetch_live_deps((pkg, version))
        mongo.insert(pkg, version, deps)

    _store_missing_live_deps(
        [dep for dep in deps if (not mongo.exists(*dep))]
    )
    for (pkg_, version_) in deps:
        # recursion step
        version_ = _clean_version(version_)
        sub_subdeps = {}
        result[to_json_key(pkg_, version_)] = sub_subdeps
        _fetch_deps(pkg_, version_, sub_subdeps)


def fetch_deps(pkg, version):
    sub_deps = {}
    result = {to_json_key(pkg, version): sub_deps}
    _fetch_deps(pkg, version, sub_deps)
    return result


def translate_latest_version(pkg):
    metadata = _fetch_live_metadata(pkg, 'latest')
    version = _clean_version(metadata['version'])
    if (not mongo.exists(pkg, version)):
        deps = [
            (p, _clean_version(v))
            for p, v in
            metadata.get('dependencies', {}).items()
        ]
        _store_missing_live_deps(
            [dep for dep in deps if (not mongo.exists(*dep))]
        )
    return version
