
from dal import DbInterface


MAX_SIZE = 1000


class CacheClient(DbInterface):

    def __init__(self, max_size=MAX_SIZE):
        self._max_size = max_size
        self._data = {}

    def get(self, json_key):
        return self._data.get(json_key)

    def insert(self, json_key, deps):
        if len(self._data) >= self._max_size:
            key = next(iter(self._data.keys()))
            del self._data[key]
        self._data[json_key] = deps


cache = CacheClient()
