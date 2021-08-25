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


############################### message_send ###################################


def test_server_send_valid(_url, _clear, _user_1, _channel_1):
    """ Test for server message_send whether is valid """
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


def test_server_send_invalid_message(_url, _clear, _user_1, _channel_1):
    """ Test for server message_send whether is invalid message """

    message_send_url = _url + "/message/send"

    random_string = ''.join(sample(ascii_letters + digits, randint(1, 10)))

    message_send_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": random_string * 1200,
    }
    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data
    )
    message_send_payload = message_send_resp.json()
    assert message_send_payload.get("code") == InputError.code


def test_server_send_invalid_channel_id(_url, _clear, _user_1, _channel_1):
    """ Test for server message_send whether is invalid channel id """

    message_send_url = _url + "/message/send"

    random_string = ''.join(sample(ascii_letters + digits, randint(1, 10)))
    wrong_id = _channel_1.get("channel_id") + randint(1, 10)
    message_send_post_data = {
        "token": _user_1.get("token"),
        "channel_id": wrong_id,
        "message": random_string,
    }
    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data
    )
    message_send_payload = message_send_resp.json()
    assert message_send_payload.get("code") == InputError.code


def test_server_send_invalid_user(_url, _clear, _user_1, _user_2, _channel_1):
    """ Test for server message_send whether is invalid user """

    message_send_url = _url + "/message/send"

    random_string = ''.join(sample(ascii_letters + digits, randint(1, 10)))

    message_send_post_data = {
        "token": _user_2.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": random_string,
    }
    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data
    )
    message_send_payload = message_send_resp.json()
    assert message_send_payload.get("code") == AccessError.code


############################## message_remove ##################################


def test_server_remove_valid(_url, _clear, _user_1, _channel_1):
    """ Test for server message_remove whether is valid """

    message_send_url = _url + "/message/send"
    message_remove_url = _url + "/message/remove"

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

    message_send_id = message_send_payload.get("message_id")

    message_remove_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
    }
    message_remove_resp = requests.delete(
        message_remove_url,
        json=message_remove_post_data
    )
    assert message_remove_resp.status_code == 200
    message_remove_payload = message_remove_resp.json()
    assert message_remove_payload == {}

    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data
    )
    assert message_send_resp.status_code == 200
    message_send_payload = message_send_resp.json()

    assert message_send_id == message_send_payload.get("message_id")


def test_server_remove_invalid_message_id(_url, _clear, _user_1, _channel_1):
    """ Test for server message_remove whether is invalid message id """

    message_send_url = _url + "/message/send"
    message_remove_url = _url + "/message/remove"

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

    message_send_id = message_send_payload.get("message_id")

    message_remove_post_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
    }
    message_remove_resp = requests.delete(
        message_remove_url,
        json=message_remove_post_data
    )
    assert message_remove_resp.status_code == 200
    message_remove_payload = message_remove_resp.json()
    assert message_remove_payload == {}

    message_remove_resp = requests.delete(
        message_remove_url,
        json=message_remove_post_data
    )
    message_remove_payload = message_remove_resp.json()
    assert message_remove_payload.get("code") == AccessError.code


def test_server_remove_not_authorised(_url, _clear, _user_1, _user_2, _channel_1):
    """ Test for server message_remove whether is not authorised """

    message_send_url = _url + "/message/send"
    message_remove_url = _url + "/message/remove"
    channel_invite_url = _url + "/channel/invite"
    channel_addowner_url = _url + "/channel/addowner"

    message_send_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": ''.join(sample(ascii_letters + digits, randint(1, 10))),
    }
    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data
    )
    assert message_send_resp.status_code == 200
    message_send_payload = message_send_resp.json()

    message_send_id = message_send_payload.get("message_id")

    message_remove_post_data = {
        "token": _user_2.get("token"),
        "message_id": message_send_id,
    }
    message_remove_resp = requests.delete(
        message_remove_url,
        json=message_remove_post_data
    )
    # Not a global owner should return AccessError
    message_remove_payload = message_remove_resp.json()
    assert message_remove_payload.get("code") == AccessError.code

    channel_invite_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "u_id": _user_2.get("u_id"),
    }
    channel_invite_resp = requests.post(
        channel_invite_url,
        json=channel_invite_post_data
    )
    assert channel_invite_resp.status_code == 200

    message_remove_resp = requests.delete(
        message_remove_url,
        json=message_remove_post_data
    )
    # Not a channel owner should return AccessError
    message_remove_payload = message_remove_resp.json()
    assert message_remove_payload.get("code") == AccessError.code

    channel_addowner_post_data = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "u_id": _user_2.get("u_id")
    }
    channel_addowner_resp = requests.post(
        channel_addowner_url,
        json=channel_addowner_post_data
    )
    assert channel_addowner_resp.status_code == 200

    message_remove_resp = requests.delete(
        message_remove_url,
        json=message_remove_post_data
    )
    assert message_remove_resp.status_code == 200

    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data
    )
    assert message_send_resp.status_code == 200
    message_send_payload = message_send_resp.json()

    assert message_send_id == message_send_payload.get("message_id")


def test_server_remove_message_owner(_url, _clear, _user_1, _user_2, _channel_1):
    """ Test for server message_remove whether is a message owner """

    message_send_url = _url + "/message/send"
    message_remove_url = _url + "/message/remove"
    channel_invite_url = _url + "/channel/invite"

    channel_invite_post_data = {
        "token": _user_1.get("token"),
        "channel_id":  _channel_1.get("channel_id"),
        "u_id": _user_2.get("u_id"),
    }
    channel_invite_resp = requests.post(
        channel_invite_url,
        json=channel_invite_post_data
    )
    assert channel_invite_resp.status_code == 200
    channel_invite_payload = channel_invite_resp.json()
    assert channel_invite_payload == {}

    message_send_post_data_1 = {
        "token": _user_2.get("token"),
        "channel_id":  _channel_1.get("channel_id"),
        "message": "Ciallo",
    }
    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data_1
    )
    assert message_send_resp.status_code == 200
    message_send_payload = message_send_resp.json()

    message_send_id = message_send_payload.get("message_id")

    message_remove_post_data = {
        "token": _user_2.get("token"),
        "message_id": message_send_id,
    }
    message_remove_resp = requests.delete(
        message_remove_url,
        json=message_remove_post_data
    )
    assert message_remove_resp.status_code == 200
    message_remove_payload = message_remove_resp.json()
    assert message_remove_payload == {}

    message_send_post_data_2 = {
        "token": _user_2.get("token"),
        "channel_id":  _channel_1.get("channel_id"),
        "message": "Ciallo",
    }
    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data_2
    )
    assert message_send_resp.status_code == 200
    message_send_payload = message_send_resp.json()

    assert message_send_id == message_send_payload.get("message_id")


################################ message_edit ##################################


def test_server_edit_valid(_url, _clear, _user_1, _channel_1):
    """ Test for server message_edit whether is valid """

    message_send_url = _url + "/message/send"
    message_edit_url = _url + "/message/edit"
    channel_messages_url = _url + "/channel/messages"

    for i in range(randint(1, 10)):
        message_send_post_data = {
            "token": _user_1.get("token"),
            "channel_id": _channel_1.get("channel_id"),
            "message": ''.join(sample(ascii_letters + digits, randint(i, 10)))
        }
        message_send_resp = requests.post(
            message_send_url,
            json=message_send_post_data
        )
        assert message_send_resp.status_code == 200

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

    message_send_id = message_send_payload.get("message_id")

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
    assert channel_messages_payload.get("end") == -1

    message_list = list(
        map(lambda x: x.get("message"), channel_messages_payload.get("messages"))
    )

    assert random_string in message_list

    message_edit_put_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "message": "Ciallo",
    }
    message_edit_resp = requests.put(
        message_edit_url,
        json=message_edit_put_data
    )
    assert message_edit_resp.status_code == 200

    channel_messages_resp = requests.get(
        channel_messages_url,
        params=channel_messages_get_data
    )
    assert channel_messages_resp.status_code == 200
    channel_messages_payload = channel_messages_resp.json()

    for i in channel_messages_payload.get("messages"):
        if i.get("message_id") == message_send_id:
            assert i.get("message") == "Ciallo"


def test_server_edit_empty_string(_url, _clear, _user_1, _channel_1):
    """ Test for server message_edit whether is an empty string """

    message_send_url = _url + "/message/send"
    message_edit_url = _url + "/message/edit"

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

    message_send_id = message_send_payload.get("message_id")

    message_edit_put_data = {
        "token": _user_1.get("token"),
        "message_id": message_send_id,
        "message": "",
    }
    message_edit_resp = requests.put(
        message_edit_url,
        json=message_edit_put_data
    )
    assert message_edit_resp.status_code == 200
    message_edit_payload = message_edit_resp.json()
    assert message_edit_payload == {}

    message_send_resp = requests.post(
        message_send_url,
        json=message_send_post_data
    )
    assert message_send_resp.status_code == 200
    message_send_payload = message_send_resp.json()

    assert message_send_id == message_send_payload.get("message_id")


def test_server_edit_invalid(_url, _clear, _user_1, _user_2, _channel_1):
    """ Test for server message_edit whether is invalid """

    message_send_url = _url + "/message/send"
    message_edit_url = _url + "/message/edit"

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

    message_send_id = message_send_payload.get("message_id")

    message_edit_put_data = {
        "token": _user_2.get("token"),
        "message_id": message_send_id,
        "message": "",
    }
    message_edit_resp = requests.put(
        message_edit_url,
        json=message_edit_put_data
    )
    message_edit_payload = message_edit_resp.json()
    assert message_edit_payload.get("code") == AccessError.code
