
import concurrent
import json

import pymongo
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from dal import to_json_key
from dal.mongo_client import mongo
from dal.cache_client import cache


NPM_REGISTRY_FMT = 'https://registry.npmjs.org/{pkg}/{version}'


class DepTree(object):

    def __init__(self, pkg, version):
        self._pkg = pkg
        self._version = self._get_version(version)
        self._json_key = to_json_key(pkg, self._version)
        self._tree = {self._json_key: {}}

    @property
    def branches(self):
        return self._tree[self._json_key]

    @property
    def tree(self):
        return self._tree

    @property
    def version(self):
        return self._version

    @property
    def json_key(self):
        return self._json_key

    def populate(self):
        mem_cached_deps = cache.get(self._json_key)
        if mem_cached_deps:
            self._tree[self._json_key] = mem_cached_deps
            return

        db_cached_deps = mongo.get(self._json_key)
        if db_cached_deps is not None:
            self._tree[self._json_key] = db_cached_deps
            return

        def _populate(key):
            dt = DepTree(*key)
            dt.populate()
            self.branches[dt.json_key] = dt.branches

        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(_populate, self._get_direct_nodes()))

        cache.insert(self._json_key, self.branches)
        try:
            mongo.insert(self._json_key, self.branches)
        except pymongo.errors.DuplicateKeyError:
            pass

    def _get_version(self, version):
        if version == 'latest':
            metadata = self._fetch_live_metadata(version)
            return self._clean_version(metadata['version'])
        return version

    def _get_direct_nodes(self):
        """[(pkg, version), (pkg, version), ...]"""
        metadata = self._fetch_live_metadata(self._version)
        dependencies = metadata.get('dependencies', {})
        return [(p, self._clean_version(v)) for p, v in dependencies.items()]

    def _fetch_live_metadata(self, version):
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)

        session.mount('https://', adapter)
        response = session.get(
            NPM_REGISTRY_FMT.format(pkg=self._pkg, version=version)
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return {}
        return response.json()

    @staticmethod
    def _clean_version(version):
        v = version.replace('~', '')
        v = version.replace('^', '')
        if '>' in v:
            v = v[v.find(' '):]
        if '<' in v:
            v = v[:v.find('')]
        return v
