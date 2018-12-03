
import os
import subprocess
import time

import pytest
import requests


API_FMT = 'http://localhost:8080/api/{pkg}/{version}'


def _get(pkg, version):
    return requests.get(API_FMT.format(pkg=pkg, version=version))


def test_accepts_1_3_5(env):
    EXPECTED = {
        "accepts@1,3,5":
            {"mime-types@2,1,18": {"mime-db@1,33,0": {}}, "negotiator@0,6,1": {}}
    }
    assert _get('accepts', '1.3.5').json() == EXPECTED


def test_non_existent_pkg(env):
    assert _get('this-does-not-exist', 'latest').status_code == 500


def test_non_existent_version(env):
    assert _get('express', 'over-9000').status_code == 500
