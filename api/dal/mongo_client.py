
import os

from pymongo import MongoClient

from dal import DbInterface
from dal import to_json_key
from dal import from_json_key


DEPENDENCIES = 'dependencies'
DEP_VIEW = 'dep-view'


class MongoInterface(DbInterface):

    def __init__(self):
        self._client_0 = MongoClient('db-a-i')
        self._client_1 = MongoClient('db-j-q')
        self._client_2 = MongoClient('db-r-z')

    def get(self, pkg, version):
        try:
            deps = self._collection(pkg).find_one(
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
        self._collection(pkg).insert_one(
            {'_id': key,
            DEPENDENCIES: [to_json_key(*dep) for dep in deps]}
        )

    def _get_client(self, pkg):
        first_letter = pkg[0]
        if 'i' >= first_letter >= 'a':
            return self._client_0
        elif 'j' >= first_letter >= 'q':
            return self._client_1
        return self._client_2

    def _collection(self, pkg):
        return self._get_client(pkg)[DEP_VIEW][DEPENDENCIES]

mongo = MongoInterface()
