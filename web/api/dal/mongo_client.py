
import os

from pymongo import MongoClient

from dal import DbInterface
from dal import to_json_key
from dal import from_json_key


DEPENDENCIES = 'dependencies'
DEP_VIEW = 'dep-view'


class MongoInterface(DbInterface):

    def __init__(self):
        self._client = MongoClient('db')

    def get(self, pkg, version):
        try:
            deps = self._collection().find_one(
                {'_id': to_json_key(pkg, version)}
            )[DEPENDENCIES]
        except TypeError:
            return None
        return [from_json_key(dep) for dep in deps]

    def exists(self, pkg, version):
        if self.get(pkg, version) is None:
            return False
        return True

    def insert(self, pkg, version, deps):
        key = to_json_key(pkg, version)
        self._collection().insert_one(
            {'_id': key,
            DEPENDENCIES: [to_json_key(*dep) for dep in deps]}
        )

    def _collection(self):
        return self._client[DEP_VIEW][DEPENDENCIES]

mongo = MongoInterface()
