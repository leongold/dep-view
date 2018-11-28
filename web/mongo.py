
from pymongo import MongoClient
client = MongoClient()


DEPENDENCIES = 'dependencies'
DEP_VIEW = 'dep-view'
COLLECTION = client[DEP_VIEW][DEPENDENCIES]
DELIM = ','


def to_json_key(pkg, version):
    return pkg + DELIM + version


def from_json_key(key):
    return tuple(key.split(DELIM))


def get(pkg, version):
    try:
        deps = COLLECTION.find_one(
            {'_id': to_json_key(pkg, version)}
        )[DEPENDENCIES]
    except TypeError:
        return None
    return [from_json_key(dep) for dep in deps]


def exists(pkg, version):
    if get(pkg, version) is None:
        return False
    return True


def insert(pkg, version, deps):
    key = to_json_key(pkg, version)
    COLLECTION.insert_one(
        {'_id': key,
         DEPENDENCIES: [to_json_key(*dep) for dep in deps]}
    )
