
import os
import subprocess
import time

import pytest
import requests


TIMEOUT = 30


@pytest.fixture
def api():
    def wait_for_api():
        start = time.time()
        while True:
            try:
                requests.get('http://localhost:8080/ping')
                time.sleep(0.5)
            except requests.exceptions.ConnectionError:
                if time.time() - start >= TIMEOUT:
                    raise ValueError('failed to run api server')
                continue
            return

    cwd = os.path.dirname(os.path.realpath(__file__))
    subprocess.Popen([os.path.join(cwd, 'run.sh')])
    wait_for_api()
    yield
    p = subprocess.Popen(['docker-compose', 'down'])
    p.wait()


def test_accepts_1_3_5(api):
    EXPECTED = {
        "accepts,1.3.5":
            {"mime-types,2.1.18": {"mime-db,1.33.0": {}}, "negotiator,0.6.1": {}}
    }
    response = requests.get('http://localhost:8080/accepts/1.3.5')
    assert response.json() == EXPECTED
