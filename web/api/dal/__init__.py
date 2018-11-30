
DELIM = '@'


def to_json_key(pkg, version):
    return pkg + DELIM + version


def from_json_key(key):
    return tuple(key.split(DELIM))


class DbInterface(object):

    def get(self, pkg, version):
        raise NotImplementedError()

    def exists(self, pkg, version):
        raise NotImplementedError()

    def insert(self, pkg, version, deps):
        raise NotImplementedError()
