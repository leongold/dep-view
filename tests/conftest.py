
import os
import subprocess
import time

import pytest
import requests


TIMEOUT = 60


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
                    raise ValueError('failed to create env')
                continue
            return

    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    subprocess.Popen([os.path.join(root, 'up.sh')])
    wait_for_env()
    yield
    p = subprocess.Popen([os.path.join(root, 'down.sh')])
    p.wait()
