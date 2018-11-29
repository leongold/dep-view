
DELIM = '@'


def to_json_key(pkg, version):
    version = version.replace('.', ',')
    pkg = pkg.replace('.', ',')
    return pkg + DELIM + version


class DbInterface(object):

    def get(self, pkg, version):
        raise NotImplementedError()

    def insert(self, pkg, version, deps):
        raise NotImplementedError()
