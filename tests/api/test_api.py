
import os
import subprocess
import time

import pytest
import requests


def test_accepts_1_3_5(env):
    EXPECTED = {
        "accepts@1,3,5":
            {"mime-types@2,1,18": {"mime-db@1,33,0": {}}, "negotiator@0,6,1": {}}
    }
    response = requests.get('http://localhost:8080/api/accepts/1.3.5')
    assert response.json() == EXPECTED
