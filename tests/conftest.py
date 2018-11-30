
import os
import subprocess
import time

import pytest
import requests


TIMEOUT = 30


@pytest.fixture
def env():
    def wait_for_env():
        start = time.time()
        while True:
            try:
                requests.get('http://localhost:8080/ping')
                requests.get('http://localhost:8080/api/ping')
                time.sleep(0.5)
            except requests.exceptions.ConnectionError:
                if time.time() - start >= TIMEOUT:
                    raise ValueError('failed to run api server')
                continue
            return

    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    subprocess.Popen([os.path.join(root, 'run.sh')])
    wait_for_env()
    yield
    p = subprocess.Popen(['docker-compose', 'down'], cwd=root)
    p.wait()
