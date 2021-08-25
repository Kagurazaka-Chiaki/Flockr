"""temporaty http test for channels.py by haotian"""
import re
import signal
from time import sleep
from subprocess import Popen, PIPE

import pytest
import requests
from error import InputError, AccessError


@pytest.fixture()
def _url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    # Use This On CSE
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    # For Windows Only
    # server = Popen(["python", "src\\server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    # Get Last Line, For Debug Only
    while not bool(local_url):
        line = server.stderr.readline()
        local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)  # url = local_url.group(1)
        # Terminate the server
        # server.send_signal(signal.SIGINT) -> (Ctrl + C)
        # For Windows and Linux
        server.send_signal(signal.SIGTERM)
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


def test_channels_create_correct(_url):
    """
    test channels/create correct conditions
    """
    data_three = requests.delete(f"{_url}/clear")
    requests.post(f"{_url}/auth/register", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })

    data_two = requests.post(f"{_url}/auth/login", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
    })
    info_two = data_two.json()

    data_three = requests.post(f"{_url}/channels/create", json={
        "token": info_two.get("token"),
        "name": "test channels",
        "is_public": True,
    })
    info_three = data_three.json()

    data_four = requests.post(f"{_url}/channels/create", json={
        "token": info_two.get("token"),
        "name": "test channels",
        "is_public": True,
    })
    info_four = data_four.json()

    assert info_three.get("channel_id") != info_four.get("channel_id")


def test_channels_create_invalid_name(_url):
    """
    test channel/create for condition of long name
    """
    requests.delete(f"{_url}/clear")
    data_one = requests.post(f"{_url}/auth/register", json={
        "email": "2lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })

    info_one = data_one.json()

    data_two = requests.post(f"{_url}/channels/create", json={
        "token": info_one.get("token"),
        "name": "this_is_too_long_name_which_has_more_than_fifty_characters",
        "is_public": True,
    })

    info_two = data_two.json()

    assert info_two.get("code") == InputError.code
    # assert info_two.get("message") == "<p>Invalid Name</p>"


def test_channels_create_invalid_token(_url):
    """
    test for invalid token conditon for channels_create function
    """

    requests.delete(f"{_url}/clear")
    data_one = requests.post(f"{_url}/auth/register", json={
        "email": "2lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_one = data_one.json()
    new_token = info_one.get("token") + "a"
    data_two = requests.post(f"{_url}/channels/create", json={
        "token": new_token,
        "name": "test channel",
        "is_public": True,
    })

    info_two = data_two.json()

    assert info_two.get("code") == AccessError.code
    # assert info_two.get("message") == "<p>Invalid Token</p>"


def test_channels_list_invalid_token(_url):
    """
    test for invalid token condition for channels_list in channels.py
    """
    requests.delete(f"{_url}/clear")
    data_one = requests.post(f"{_url}/auth/register", json={
        "email": "2lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_one = data_one.json()
    new_token = info_one.get("token")
    requests.post(f"{_url}/channels/create", json={
        "token": new_token,
        "name": "test channel",
        "is_public": True,
    })
    wrong_token = new_token + "a"
    data_three = requests.get(
        f"{_url}/channels/list", params={"token": wrong_token})
    info_three = data_three.json()

    assert info_three.get("code") == AccessError.code
    # assert info_three.get("message") == "<p>Invalid token</p>"


def test_channels_list_correct(_url):
    """
    test for correct condition for channels_list in channels.py
    """

    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "2lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_one = user_one.json()
    new_token = info_one.get("token")
    requests.post(f"{_url}/channels/create", json={
        "token": new_token,
        "name": "test channel1",
        "is_public": True,
    })
    requests.post(f"{_url}/channels/create", json={
        "token": new_token,
        "name": "test channel2",
        "is_public": True,
    })

    data_three = requests.get(
        f"{_url}/channels/list", params={"token": new_token})
    info_three = data_three.json()
    list_channel = info_three.get("channels")
    assert len(list_channel) == 2

    user_two = requests.post(f"{_url}/auth/register", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_two = user_two.json()
    token_two = info_two.get("token")

    requests.post(f"{_url}/channels/create", json={
        "token": token_two,
        "name": "test channel3",
        "is_public": True,
    })

    data_three = requests.get(
        f"{_url}/channels/list", params={"token": new_token})
    info_three = data_three.json()
    list_channel = info_three.get("channels")
    assert len(list_channel) == 2

    data_three = requests.get(
        f"{_url}/channels/list", params={"token": token_two})
    info_three = data_three.json()
    list_channel = info_three.get("channels")
    assert len(list_channel) == 1


def test_channels_listall_correct(_url):
    """
    test for invalid token condition for channels_listall in channels.py
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_one = user_one.json()
    new_token = info_one.get("token")
    requests.post(f"{_url}/channels/create", json={
        "token": new_token,
        "name": "test channel1",
        "is_public": True,
    })
    requests.post(f"{_url}/channels/create", json={
        "token": new_token,
        "name": "test channel2",
        "is_public": True,
    })

    data_three = requests.get(
        f"{_url}/channels/listall", params={"token": new_token})
    info_three = data_three.json()
    list_channel = info_three.get("channels")
    assert len(list_channel) == 2

    user_two = requests.post(f"{_url}/auth/register", json={
        "email": "dfslyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_two = user_two.json()
    token_two = info_two.get("token")

    requests.post(f"{_url}/channels/create", json={
        "token": token_two,
        "name": "test channel3",
        "is_public": True,
    })

    data_three = requests.get(
        f"{_url}/channels/listall", params={"token": new_token})
    info_three = data_three.json()
    list_channel = info_three.get("channels")
    assert len(list_channel) == 3

    data_three = requests.get(
        f"{_url}/channels/listall", params={"token": token_two})
    info_three = data_three.json()
    list_channel = info_three.get("channels")
    assert len(list_channel) == 3


def test_channels_listall_invalid_token(_url):
    """
    test for invalid token condition for channels_listall in channels.py
    """
    requests.delete(f"{_url}/clear")
    data_one = requests.post(f"{_url}/auth/register", json={
        "email": "2lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_one = data_one.json()
    new_token = info_one.get("token")
    requests.post(f"{_url}/channels/create", json={
        "token": new_token,
        "name": "test channel",
        "is_public": True,
    })
    wrong_token = new_token + "a"
    data_three = requests.get(
        f"{_url}/channels/listall", params={"token": wrong_token})
    info_three = data_three.json()

    assert info_three.get("code") == AccessError.code
    # assert info_three.get("message") == "<p>Invalid token</p>"
