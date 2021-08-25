# -*- coding: utf-8 -*-
""" HTTP tests for standup.py """

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



def test_valid_standup_start(_url):
    """
    Test the correct conditions for http function standup start
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    ch_info = ch_info.json()

    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "length": 30,
    })
    assert standup_start.status_code == 200
    standup_start = standup_start.json()

    standup_info = requests.get(f"{_url}/standup/active", params={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
    })
    assert standup_info.status_code == 200
    standup_info = standup_info.json()

    assert standup_info["is_active"]

def test_invalid_channel_id_standup_start(_url):
    """
    Test the error conditions(Invalid channel_id)
    for http function standup_start
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_one["token"],
        "channel_id": 2,
        "length": 30,
    })
    standup_start = standup_start.json()
    assert standup_start["code"] == InputError.code

def test_already_running_standup_start(_url):
    """
    Test the error conditions(standup is already active in the channel)
    for http function standup_start
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    assert user_one.status_code == 200
    user_one = user_one.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    assert ch_info.status_code == 200
    ch_info = ch_info.json()

    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "length": 30,
    })
    assert standup_start.status_code == 200
    standup_start = standup_start.json()

    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "length": 30,
    })
    standup_start = standup_start.json()
    assert standup_start["code"] == InputError.code

def test_not_a_member_standup_start(_url):
    """
    Test the error conditions(user is not a member in the channel)
    for http function standup_start
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    assert user_one.status_code == 200
    user_one = user_one.json()

    user_two = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark",
    })
    assert user_two.status_code == 200
    user_two = user_two.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    assert ch_info.status_code == 200
    ch_info = ch_info.json()

    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_two["token"],
        "channel_id": ch_info["channel_id"],
        "length": 30,
    })
    standup_start = standup_start.json()
    assert standup_start["code"] == InputError.code

def test_valid_standup_active(_url):
    """
    Test the correct conditions for http function standup active
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    assert user_one.status_code == 200
    user_one = user_one.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    assert ch_info.status_code == 200
    ch_info = ch_info.json()
    # test for standup not running
    standup_info = requests.get(f"{_url}/standup/active", params={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
    })
    assert standup_info.status_code == 200
    standup_info = standup_info.json()

    assert not standup_info["is_active"]
    assert standup_info["time_finish"] is None

    # test for standup running
    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "length": 30,
    })
    assert standup_start.status_code == 200
    standup_start = standup_start.json()

    standup_info = requests.get(f"{_url}/standup/active", params={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
    })
    standup_info = standup_info.json()

    assert standup_info["is_active"]
    assert standup_info["time_finish"] == standup_start["time_finish"]

def test_invalid_channel_id_standup_active(_url):
    """
    Test the error conditions(Invalid channel_id)
    for http function standup_active
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    standup_info = requests.get(f"{_url}/standup/active", params={
        "token": user_one["token"],
        "channel_id": 2,
    })
    standup_info = standup_info.json()
    assert standup_info["code"] == InputError.code

def test_invalid_token_standup_active(_url):
    """
    Test the error conditions(Invalid token)
    for http function standup_active
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    ch_info = ch_info.json()

    standup_info = requests.get(f"{_url}/standup/active", params={
        "token": "some_token",
        "channel_id": ch_info["channel_id"],
    })
    standup_info = standup_info.json()
    assert standup_info["code"] == AccessError.code

def test_valid_standup_send(_url):
    """
    Test the correct conditions for http function standup send
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    user_two = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark",
    })
    user_two = user_two.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    assert ch_info.status_code == 200
    ch_info = ch_info.json()

    ch_join = requests.post(f"{_url}/channel/join", json={
        "token": user_two["token"],
        "channel_id": ch_info["channel_id"],
    })
    assert ch_join.status_code == 200
    ch_join = ch_join.json()

    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "length": 5,
    })
    assert standup_start.status_code == 200
    standup_start = standup_start.json()

    standup_send = requests.post(f"{_url}/standup/send", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "message": "Hello",
    })
    assert standup_send.status_code == 200

    requests.post(f"{_url}/standup/send", json={
        "token": user_two["token"],
        "channel_id": ch_info["channel_id"],
        "message": "Hi",
    })

    requests.post(f"{_url}/standup/send", json={
        "token": user_two["token"],
        "channel_id": ch_info["channel_id"],
        "message": "How are you?",
    })

    requests.post(f"{_url}/standup/send", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "message": "Thank You",
    })
    sleep(5)

    standup_info = requests.get(f"{_url}/standup/active", params={
        "token": user_two["token"],
        "channel_id": ch_info["channel_id"],
    })
    standup_info = standup_info.json()

    assert not standup_info["is_active"]
    assert standup_info["time_finish"] is None

    mess_info = requests.get(f"{_url}/channel/messages", params={
        "token": user_two["token"],
        "channel_id": ch_info["channel_id"],
        "start": 0,
    })
    assert mess_info.status_code == 200
    mess_info = mess_info.json()
    assert len(mess_info["messages"]) == 1

def test_invalid_channel_id_standup_send(_url):
    """
    Test the error conditions(Invalid channel id)
    for http function standup_send
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    standup_send = requests.post(f"{_url}/standup/send", json={
        "token": user_one["token"],
        "channel_id": 2,
        "message": "Hello",
    })
    standup_send = standup_send.json()
    assert standup_send["code"] == InputError.code

def test_invalid_message_standup_send(_url):
    """
    Test the error conditions(Invalid message length)
    for http function standup_send
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    ch_info = ch_info.json()

    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "length": 30,
    })
    standup_start = standup_start.json()

    message = "hello" * 1000

    standup_send = requests.post(f"{_url}/standup/send", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "message": message,
    })
    standup_send = standup_send.json()
    assert standup_send["code"] == InputError.code

def test_no_active_standup_send(_url):
    """
    Test the error conditions(no active standup in the channel)
    for http function standup_send
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    ch_info = ch_info.json()

    standup_send = requests.post(f"{_url}/standup/send", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "message": "message",
    })
    standup_send = standup_send.json()
    assert standup_send["code"] == InputError.code

def test_not_a_member_standup_send(_url):
    """
    Test the error conditions(user is not a member in the channel)
    for http function standup_send
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "simple@example.org",
        "password": "123456",
        "name_first": "sh",
        "name_last": "LA",
    })
    user_one = user_one.json()

    user_two = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark",
    })
    user_two = user_two.json()

    ch_info = requests.post(f"{_url}/channels/create", json={
        "token": user_one["token"],
        "name": "test channel",
        "is_public": True,
    })
    ch_info = ch_info.json()

    standup_start = requests.post(f"{_url}/standup/start", json={
        "token": user_one["token"],
        "channel_id": ch_info["channel_id"],
        "length": 30,
    })
    assert standup_start.status_code == 200

    standup_send = requests.post(f"{_url}/standup/send", json={
        "token": user_two["token"],
        "channel_id": ch_info["channel_id"],
        "message": "message",
    })
    standup_send = standup_send.json()
    assert standup_send["code"] == AccessError.code
