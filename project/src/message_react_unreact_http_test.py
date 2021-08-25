# -*- coding: utf-8 -*-
""" Tests for server.py """

import re
import json
import signal
from random import randint, sample
from string import ascii_letters, digits
from time import sleep
from subprocess import Popen, PIPE

import pytest
import requests
from error import InputError


# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
# Add _ perfix for fixture function to avoid pylint
@pytest.fixture()
def _url():
    """ Get the URL of the server """
    url_re = re.compile(r' \* Running on ([^ ]*)')
    # Use This On CSE
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    #server = Popen(["python3", "temp_server_sx.py"], stderr=PIPE, stdout=PIPE)
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


@pytest.fixture()
def _message_send_1(_url, _user_1, _channel_1):
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
    Then send a random message in the channel
    """
    message_send_url = _url + "/message/send"
    random_string = ''.join(sample(ascii_letters + digits, randint(1, 10)))

    message_send_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": random_string,
    }
    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data
    )
    assert message_send_resp.status_code == 200
    message_send_payload = message_send_resp.json()
    assert message_send_payload != {}

    yield message_send_payload

############################### message_react ###################################

def test_sever_invalid_react_id(_url, _clear, _user_1, _channel_1, _message_send_1):
    """ test invalid react_id situation for message_react """

    message_react_url = _url +"/message/react"
    message_send_id = _message_send_1.get("message_id")

    message_react_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 2,
    }
    message_react_resp = requests.post(
        message_react_url,
        json=message_react_post_data
    )

    message_react_payload = message_react_resp.json()
    assert message_react_payload.get("code") == InputError.code


def test_message_react_not_exist(_url, _clear, _user_1, _channel_1, _message_send_1):
    """test invalid message id for message_react"""

    message_react_url = _url +"/message/react"
    message_send_id = _message_send_1.get("message_id")

    message_react_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id + 1,
        "react_id": 1,
    }
    message_react_resp = requests.post(
        message_react_url,
        json=message_react_post_data
    )

    message_react_payload = message_react_resp.json()
    assert message_react_payload.get("code") == InputError.code


def test_message_react_already_exist(_url, _clear, _user_1, _channel_1, _message_send_1):
    """test duplicate react situation for message_react"""

    message_react_url = _url +"/message/react"
    message_send_id = _message_send_1.get("message_id")

    message_react_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 1,
    }
    message_react_resp = requests.post(
        message_react_url,
        json=message_react_post_data
    )

    assert message_react_resp.status_code == 200
    message_react_post_data2 = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 1,
    }
    message_react_resp2 = requests.post(
        message_react_url,
        json=message_react_post_data2
    )

    message_react_payload2 = message_react_resp2.json()
    assert message_react_payload2.get("code") == InputError.code


def test_message_react_correct(_url, _clear, _user_1, _channel_1, _message_send_1):
    """test correct situation for message_react"""

    message_react_url = _url + "/message/react"
    channel_messages_url = _url + "/channel/messages"

    message_send_id = _message_send_1.get("message_id")

    message_react_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 1,
    }
    message_react_resp = requests.post(
        message_react_url,
        json=message_react_post_data
    )

    assert message_react_resp.status_code == 200

    channel_messages_get_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "start": 0
    }
    channel_messages_resp = requests.get(
        channel_messages_url,
        params=channel_messages_get_data
    )
    assert channel_messages_resp.status_code == 200

    channel_messages_payload = channel_messages_resp.json()
    message_list = channel_messages_payload.get("messages")
    message_dict = message_list[0]
    react_list = message_dict["reacts"]

    assert _user_1.get("u_id") in react_list[0]["u_ids"]
    assert react_list[0]["is_this_user_reacted"]


############################### message_unreact ###################################

def test_sever_invalid_unreact_id(_url, _clear, _user_1, _channel_1, _message_send_1):
    """ test invalid react_id situation for message_unreact """

    message_react_url = _url + "/message/react"
    message_unreact_url = _url +"/message/unreact"
    message_send_id = _message_send_1.get("message_id")

    message_react_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 1,
    }
    message_react_resp = requests.post(
        message_react_url,
        json=message_react_post_data
    )
    assert message_react_resp.status_code == 200

    message_unreact_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 2,
    }
    message_unreact_resp = requests.post(
        message_unreact_url,
        json=message_unreact_post_data
    )

    message_unreact_payload = message_unreact_resp.json()
    assert message_unreact_payload.get("code") == InputError.code


def test_message_unreact_not_exist(_url, _clear, _user_1, _channel_1, _message_send_1):
    """test invalid message id for message_unreact"""

    message_react_url = _url +"/message/react"
    message_unreact_url = _url +"/message/unreact"
    message_send_id = _message_send_1.get("message_id")

    message_react_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 1,
    }
    message_react_resp = requests.post(
        message_react_url,
        json=message_react_post_data
    )
    assert message_react_resp.status_code == 200

    message_unreact_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id + 1,
        "react_id": 1,
    }
    message_unreact_resp = requests.post(
        message_unreact_url,
        json=message_unreact_post_data
    )

    message_unreact_payload = message_unreact_resp.json()
    assert message_unreact_payload.get("code") == InputError.code


def test_message_unreact_already_exist(_url, _clear, _user_1, _channel_1, _message_send_1):
    """test duplicate react situation for message_unreact"""

    message_unreact_url = _url +"/message/unreact"
    message_send_id = _message_send_1.get("message_id")

    message_unreact_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 1,
    }
    message_unreact_resp = requests.post(
        message_unreact_url,
        json=message_unreact_post_data
    )

    message_unreact_payload = message_unreact_resp.json()
    assert message_unreact_payload.get("code") == InputError.code


def test_message_unreact_correct(_url, _clear, _user_1, _channel_1, _message_send_1):
    """ test correct situation for message_unreact """

    channel_messages_url = _url + "/channel/messages"
    message_react_url = _url +"/message/react"
    message_unreact_url = _url +"/message/unreact"
    message_send_id = _message_send_1.get("message_id")

    message_react_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 1,
    }
    message_react_resp = requests.post(
        message_react_url,
        json=message_react_post_data
    )
    assert message_react_resp.status_code == 200

    message_unreact_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "react_id": 1,
    }
    message_unreact_resp = requests.post(
        message_unreact_url,
        json=message_unreact_post_data
    )
    assert message_unreact_resp.status_code == 200

    channel_messages_get_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "start": 0
    }
    channel_messages_resp = requests.get(
        channel_messages_url,
        params=channel_messages_get_data
    )
    assert channel_messages_resp.status_code == 200

    channel_messages_payload = channel_messages_resp.json()
    message_list = channel_messages_payload.get("messages")
    message_dict = message_list[0]
    react_list = message_dict["reacts"]

    assert _user_1.get("u_id")  not in react_list[0]["u_ids"]
    assert not react_list[0]["is_this_user_reacted"]
