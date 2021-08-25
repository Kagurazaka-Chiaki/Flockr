"""http test for message in iteration 3 by Haotian"""
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

########################## message/pin #########################################

def test_message_pin_invalid_message_id(_url, _clear, _user_1, _channel_1):
    """ test invalid message id situation for message/pin"""
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    message_send_resp = requests.post(
        message_send_url,
        json=message_data_one
    )

    info_send = message_send_resp.json()

    message_pin_resp = requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id") + 1,
    })

    info_pin = message_pin_resp.json()

    assert info_pin.get("code") == InputError.code
    # assert info_pin.get("message") == "<p>No this message</p>"


def test_message_pin_already_pinned(_url, _clear, _user_1, _channel_1):
    """ test invalid message id situation for message/pin"""
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    message_send_resp = requests.post(
        message_send_url,
        json=message_data_one
    )

    info_send = message_send_resp.json()

    message_pin_resp = requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_pin = message_pin_resp.json()

    assert info_pin == {}
    assert message_pin_resp.status_code == 200

    message_pin_resp_two = requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_pin_two = message_pin_resp_two.json()

    assert info_pin_two.get("code") == InputError.code
    # assert info_pin_two.get("message") == "<p>Already pinned</p>"


def test_message_pin_not_member(_url, _clear, _user_1, _user_2, _channel_1):
    """ test invalid message id situation for message/pin"""
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    message_send_resp = requests.post(
        message_send_url,
        json=message_data_one
    )

    info_send = message_send_resp.json()

    message_pin_resp = requests.post(f"{_url}/message/pin", json={
        "token": _user_2.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_pin = message_pin_resp.json()

    assert info_pin.get("code") == AccessError.code
    # assert info_pin.get("message") == "<p>Not a member</p>"


def test_message_pin_not_owner(_url, _clear, _user_1, _user_2, _channel_1):
    """ test invalid message id situation for message/pin"""
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    message_send_resp = requests.post(
        message_send_url,
        json=message_data_one
    )

    info_send = message_send_resp.json()

    requests.post(f"{_url}/channel/invite", json={
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "u_id": _user_2.get("u_id"),
    })

    message_pin_resp = requests.post(f"{_url}/message/pin", json={
        "token": _user_2.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_pin = message_pin_resp.json()

    assert info_pin.get("code") == AccessError.code
    # assert info_pin.get("message") == "<p>Not a owner</p>"


def test_message_pin_correct(_url, _clear, _user_1, _channel_1):
    """ test correct situation for message/pin """
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    requests.post(
        message_send_url,
        json=message_data_one
    )

    message_send_url = _url + "/message/send"
    message_data_two = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "world",
    }

    message_send_resp_two = requests.post(
        message_send_url,
        json=message_data_two
    )

    info_send = message_send_resp_two.json()

    requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    channel_messages_data = requests.get(f"{_url}/channel/messages", params={
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "start": 0,
    })

    info_message = channel_messages_data.json()

    message_list = info_message["messages"]
    message_dict = message_list[0]
    message_dict2 = message_list[1]
    is_pin2 = message_dict2["is_pinned"]
    is_pin = message_dict["is_pinned"]
    assert is_pin
    assert not is_pin2


########################## message/unpin #######################################

def test_message_unpin_invalid_message_id(_url, _clear, _user_1, _channel_1):
    """ test invalid message id situation for message/pin"""
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    message_send_resp = requests.post(
        message_send_url,
        json=message_data_one
    )

    info_send = message_send_resp.json()

    message_pin_resp = requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_pin = message_pin_resp.json()

    assert info_pin == {}
    assert message_pin_resp.status_code == 200

    message_unpin_resp = requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id") + 1,
    })

    info_unpin = message_unpin_resp.json()

    assert info_unpin.get("code") == InputError.code
    # assert info_unpin.get("message") == "<p>No this message</p>"


def test_message_unpin_already_unpinned(_url, _clear, _user_1, _channel_1):
    """ test invalid message id situation for message/pin"""
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    message_send_resp = requests.post(
        message_send_url,
        json=message_data_one
    )

    info_send = message_send_resp.json()

    message_unpin_resp = requests.post(f"{_url}/message/unpin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_unpin = message_unpin_resp.json()

    assert info_unpin.get("code") == InputError.code
    # assert info_unpin.get("message") == "<p>Already unpinned</p>"


def test_message_unpin_not_member(_url, _clear, _user_1, _user_2, _channel_1):
    """ test invalid message id situation for message/pin"""
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    message_send_resp = requests.post(
        message_send_url,
        json=message_data_one
    )

    info_send = message_send_resp.json()

    message_pin_resp = requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_pin = message_pin_resp.json()

    assert info_pin == {}
    assert message_pin_resp.status_code == 200

    message_unpin_resp = requests.post(f"{_url}/message/unpin", json={
        "token": _user_2.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_unpin = message_unpin_resp.json()

    assert info_unpin.get("code") == AccessError.code
    # assert info_unpin.get("message") == "<p>Not a member</p>"


def test_message_unpin_not_owner(_url, _clear, _user_1, _user_2, _channel_1):
    """ test invalid message id situation for message/pin"""
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    message_send_resp = requests.post(
        message_send_url,
        json=message_data_one
    )

    info_send = message_send_resp.json()

    requests.post(f"{_url}/channel/invite", json={
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "u_id": _user_2.get("u_id"),
    })

    requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    message_unpin_resp = requests.post(f"{_url}/message/unpin", json={
        "token": _user_2.get("token"),
        "message_id": info_send.get("message_id"),
    })

    info_unpin = message_unpin_resp.json()

    assert info_unpin.get("code") == AccessError.code
    assert info_unpin.get("message") == "<p>Not a owner</p>"


def test_message_unpin_correct(_url, _clear, _user_1, _channel_1):
    """ test correct situation for message/pin """
    message_send_url = _url + "/message/send"
    message_data_one = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "Hello",
    }


    requests.post(
        message_send_url,
        json=message_data_one
    )

    message_send_url = _url + "/message/send"
    message_data_two = {
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "message": "world",
    }

    message_send_resp_two = requests.post(
        message_send_url,
        json=message_data_two
    )

    info_send = message_send_resp_two.json()

    requests.post(f"{_url}/message/pin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    channel_messages_data = requests.get(f"{_url}/channel/messages", params={
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "start": 0,
    })

    info_message = channel_messages_data.json()

    message_list = info_message["messages"]
    message_dict = message_list[0]
    message_dict2 = message_list[1]
    is_pin2 = message_dict2["is_pinned"]
    is_pin = message_dict["is_pinned"]
    assert is_pin
    assert not is_pin2

    requests.post(f"{_url}/message/unpin", json={
        "token": _user_1.get("token"),
        "message_id": info_send.get("message_id"),
    })

    channel_messages_data = requests.get(f"{_url}/channel/messages", params={
        "token": _user_1.get("token"),
        "channel_id": _channel_1.get("channel_id"),
        "start": 0,
    })

    info_message = channel_messages_data.json()

    message_list = info_message["messages"]
    message_dict = message_list[0]
    message_dict2 = message_list[1]
    is_pin2 = message_dict2["is_pinned"]
    is_pin = message_dict["is_pinned"]
    assert not is_pin
    assert not is_pin2
