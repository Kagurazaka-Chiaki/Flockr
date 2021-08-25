
import re
import json
import signal
from time import sleep
from subprocess import Popen, PIPE

import pytest

import requests


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def _url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    # server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


def test_url(_url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert _url.startswith("http")


def test_echo(_url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(_url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}
