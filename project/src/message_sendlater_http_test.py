# -*- coding: utf-8 -*-
""" Tests for server.py """

import re
import json
import signal
from random import randint, sample, choice
from string import ascii_letters, digits
from time import sleep
from subprocess import Popen, PIPE

import pytest
import requests
from datetime import timezone, datetime
from error import InputError, AccessError


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
# Add _ perfix for fixture function to avoid pylint
@pytest.fixture()
def _url():
    """ Get the URL of the server """
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


@pytest.fixture()
def _clear(_url):
    """ Clear the Data """
    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200


@pytest.fixture()
def _user_1(_url):
    """
    Register a user within the data follows
    {
        "email": "simple@example.edu",
        "password": "123456",
        "name_first": "Hayden",
        "name_last": "Jacobs",
    }
    """
    auth_register_url = _url + "/auth/register"

    auth_register_post_data = {
        "email": "simple@example.edu",
        "password": "123456",
        "name_first": "Hayden",
        "name_last": "Jacobs",
    }
    auth_register_resp = requests.post(
        auth_register_url,
        json=auth_register_post_data
    )
    assert auth_register_resp.status_code == 200
    auth_register_payload = auth_register_resp.json()

    yield auth_register_payload


@pytest.fixture()
def _user_2(_url):
    """
    Register a user within the data follows
    {
        "email": "simple@example.com",
        "password": "123456",
        "name_first": "Ian",
        "name_last": "Thorvaldson",
    }
    """
    auth_register_url = _url + "/auth/register"

    auth_register_post_data = {
        "email": "simple@example.com",
        "password": "123456",
        "name_first": "Ian",
        "name_last": "Thorvaldson",
    }
    auth_register_resp = requests.post(
        auth_register_url, json=auth_register_post_data
    )
    assert auth_register_resp.status_code == 200
    auth_register_payload = auth_register_resp.json()

    yield auth_register_payload


@pytest.fixture()
def _channel_1(_url, _user_1):
    """
    Register a user within the data follows
    {
        "email": "simple@example.com",
        "password": "123456",
        "name_first": "Ian",
        "name_last": "Thorvaldson",
    }
    And create a channel within the data follows
    {
        "token": _user_1.get("token"),
        "name": "COMP1531",
        "is_public": True,
    }
    """
    channels_create_url = _url + "/channels/create"

    channels_create_post_data = {
        "token": _user_1.get("token"),
        "name": "COMP1531",
        "is_public": True,
    }
    channels_create_resp = requests.post(
        channels_create_url,
        json=channels_create_post_data
    )
    assert channels_create_resp.status_code == 200
    channels_create_payload = channels_create_resp.json()

    yield channels_create_payload


def test_server_message_sendlater_valid(_url, _clear, _user_1, _channel_1):
    """ Test for server message_send whether is valid """

    message_sendlater_url = _url + "/message/sendlater"

    random_string = ''.join(sample(ascii_letters + digits, randint(1, 10)))

    interval = datetime.now(timezone.utc).timestamp() + 1

    message_sendlater_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": random_string * 1200,
        "time_sent": interval
    }
    message_sendlater_resp = requests.post(
        message_sendlater_url,
        json=message_sendlater_post_data
    )
    assert message_sendlater_resp.status_code == InputError.code

    message_sendlater_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": random_string,
        "time_sent": interval - 10
    }
    message_sendlater_resp = requests.post(
        message_sendlater_url,
        json=message_sendlater_post_data
    )
    assert message_sendlater_resp.status_code == InputError.code

    message_sendlater_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id") + randint(10, 20),
        "message": random_string,
        "time_sent": interval
    }
    message_sendlater_resp = requests.post(
        message_sendlater_url,
        json=message_sendlater_post_data
    )
    assert message_sendlater_resp.status_code == InputError.code

    message_sendlater_post_data = {
        "token": _user_1.get("token") + choice(ascii_letters + digits),
        "channel_id": _channel_1.get("channel_id"),
        "message": random_string * 1200,
        "time_sent": interval
    }
    message_sendlater_resp = requests.post(
        message_sendlater_url,
        json=message_sendlater_post_data
    )
    assert message_sendlater_resp.status_code == AccessError.code

    message_sendlater_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": random_string,
        "time_sent": interval
    }
    message_sendlater_resp = requests.post(
        message_sendlater_url,
        json=message_sendlater_post_data
    )
    assert message_sendlater_resp.status_code == 200
    message_sendlater_payload = message_sendlater_resp.json()
    assert message_sendlater_payload != {}
