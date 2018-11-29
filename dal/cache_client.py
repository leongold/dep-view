
from dal import DbInterface


MAX_SIZE = 1000


class CacheClient(DbInterface):

    def __init__(self, max_size=MAX_SIZE):
        self._max_size = max_size
        self._data = {}

    def get(self, pkg, version):
        return self._data.get((pkg, version), None)

    def exists(self, pkg, version):
        return (pkg, version) in self._data

    def insert(self, pkg, version, deps):
        if len(self._data) >= self._max_size:
            key = next(iter(self._data.keys()))
            del self._data[key]
        self._data[(pkg, version)] = deps


cache = CacheClient()
