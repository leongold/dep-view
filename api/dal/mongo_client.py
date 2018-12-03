
from pymongo import MongoClient

from dal import DbInterface


DEPENDENCIES = 'dependencies'
DEP_VIEW = 'dep-view'


class MongoInterface(DbInterface):

    def __init__(self):
        self._client_0 = MongoClient('db-a-i')
        self._client_1 = MongoClient('db-j-q')
        self._client_2 = MongoClient('db-r-z')

    def get(self, key):
        try:
            return self._collection(key).find_one(
                {'_id': key}
            )[DEPENDENCIES]
        except TypeError:
            return None

    def insert(self, key, deps):
        self._collection(key).insert_one({
            '_id': key,
            DEPENDENCIES: deps
        })

    def _get_client(self, first_letter):
        if 'i' >= first_letter >= 'a':
            return self._client_0
        elif 'j' >= first_letter >= 'q':
            return self._client_1
        return self._client_2

    def _collection(self, key):
        return self._get_client(key[0])[DEP_VIEW][DEPENDENCIES]


mongo = MongoInterface()
