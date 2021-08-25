""" http test for user file """
#import json
import re
import signal
from time import sleep
from subprocess import Popen, PIPE

import pytest
import requests
from error import InputError

# Use this fixture to get the _url of the server. It starts the server for you,
# so you don't need to.


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


@pytest.fixture()
def _clear(_url):
    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200


def test_url(_url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert _url.startswith("http")


def test_user_profile_invalid_token(_url):
    """this will test invalid u_id"""
    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_data_1 = {
        "token": "invalid token",
        "u_id": auth_register_payload_1.get("u_id")
    }
    user_profile_resp_1 = requests.get(
        _url + "/user/profile", params=user_profile_data_1
    )

    assert user_profile_resp_1.status_code == InputError.code


def test_user_profile_invalid_uid(_url):
    """this will test invalid token"""
    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "u_id": auth_register_payload_1.get("u_id") + 1,
    }
    user_profile_resp_1 = requests.get(
        _url + "/user/profile", params=user_profile_data_1
    )

    assert user_profile_resp_1.status_code == InputError.code


def test_user_profile(_url):
    """ this will test whether user_profile_setname can work or not"""
    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    auth_register_post_data_2 = {
        'email': 'simple2@email.com',
        'password': '12345678sdf',
        'name_first': 'Ming',
        'name_last': 'Kai',
    }

    auth_register_resp_2 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_2
    )
    assert auth_register_resp_2.status_code == 200

    auth_register_payload_2 = auth_register_resp_2.json()

    user_profile_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "u_id": auth_register_payload_2.get("u_id"),
    }
    user_profile_resp_1 = requests.get(
        _url + "/user/profile", params=user_profile_data_1
    )
    assert user_profile_resp_1.status_code == 200
    user_profile_payload_1 = user_profile_resp_1.json()

    assert user_profile_payload_1["user"].get(
        "email") == auth_register_post_data_2["email"]
    assert (user_profile_payload_1["user"].get("name_first") ==
            auth_register_post_data_2["name_first"])
    assert user_profile_payload_1["user"].get(
        "name_last") == auth_register_post_data_2["name_last"]
    assert user_profile_payload_1["user"].get(
        "u_id") == auth_register_payload_2.get("u_id")


def test_user_profile_setname_invalid_name(_url):
    """ this will test name_first/name_last
    is not between 1 and 50 characters inclusively in length"""

    # wrong situation for invalid name_first

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_setname_put_data = {
        "token": auth_register_payload_1.get("token"),
        "name_first": "",
        "name_last": "ValidLastName",
    }
    user_profile_setname_resp_1 = requests.put(
        _url + "/user/profile/setname", json=user_profile_setname_put_data
    )
    assert user_profile_setname_resp_1.status_code == InputError.code

    # wrong situation for invalid name_last

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_setname_put_data = {
        "token": auth_register_payload_1.get("token"),
        "name_first": "ValidFirstName",
        "name_last": "",
    }
    user_profile_setname_resp_1 = requests.put(
        _url + "/user/profile/setname", json=user_profile_setname_put_data
    )
    assert user_profile_setname_resp_1.status_code == InputError.code


def test_user_profile_setname_invalid_token(_url):
    """this will test invalid token"""

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }
    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    user_profile_setname_put_data = {
        "token": "invalid token",
        "name_first": "ValidFirstName",
        "name_last": "ValidLastName",
    }
    user_profile_setname_resp_1 = requests.put(
        _url + "/user/profile/setname", json=user_profile_setname_put_data
    )
    assert user_profile_setname_resp_1.status_code == InputError.code


def test_user_profile_setname_correct(_url):
    """ this will test whether user_profile_setname can work or not """

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_setname_put_data = {
        "token": auth_register_payload_1.get("token"),
        "name_first": "NewFirstName",
        "name_last": "NewLastName",
    }
    user_profile_setname_resp_1 = requests.put(
        _url + "/user/profile/setname", json=user_profile_setname_put_data
    )
    assert user_profile_setname_resp_1.status_code == 200

    user_profile_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "u_id": auth_register_payload_1.get("u_id"),
    }
    user_profile_resp_1 = requests.get(
        _url + "/user/profile", params=user_profile_data_1
    )
    assert user_profile_resp_1.status_code == 200

    user_profile_payload_1 = user_profile_resp_1.json()
    assert user_profile_payload_1["user"].get("name_first") == "NewFirstName"
    assert user_profile_payload_1["user"].get("name_last") == "NewLastName"


def test_user_profile_setemail_invalid_email(_url):
    """ this will test Email entered is not a valid email """

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_setemail_put_data = {
        "token": auth_register_payload_1.get("token"),
        "email": "invalid email"
    }
    user_profile_setemail_resp_1 = requests.put(
        _url + "/user/profile/setemail", json=user_profile_setemail_put_data
    )
    assert user_profile_setemail_resp_1.status_code == InputError.code


def test_user_profile_setemail_used_email(_url):
    """ this will test Email address is already being used by another user """

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    # create another user for preparing for a used email
    auth_register_post_data_2 = {
        'email': 'simple2@email.com',
        'password': '12345678sdf',
        'name_first': 'Ming',
        'name_last': 'Kai',
    }

    auth_register_resp_2 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_2
    )
    assert auth_register_resp_2.status_code == 200

    user_profile_setemail_put_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "email": auth_register_post_data_2.get("email")
    }
    user_profile_setemail_resp_1 = requests.put(
        _url + "/user/profile/setemail", json=user_profile_setemail_put_data_1
    )
    assert user_profile_setemail_resp_1.status_code == InputError.code


def test_user_profile_setemail_invalid_token(_url):
    """this will test invalid token"""

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    user_profile_setemail_put_data_1 = {
        "token": "invalid token",
        "email": "validemail@email.com"
    }
    user_profile_setemail_resp_1 = requests.put(
        _url + "/user/profile/setemail", json=user_profile_setemail_put_data_1
    )
    assert user_profile_setemail_resp_1.status_code == InputError.code


def test_user_profile_setemail_correct(_url):
    """ this will test whether user_profile_setemail can work or not"""

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }

    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_setemail_put_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "email": "validemail@email.com"
    }
    user_profile_setemail_resp_1 = requests.put(
        _url + "/user/profile/setemail", json=user_profile_setemail_put_data_1
    )
    assert user_profile_setemail_resp_1.status_code == 200

    user_profile_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "u_id": auth_register_payload_1.get("u_id"),
    }
    user_profile_resp_1 = requests.get(
        _url + "/user/profile", params=user_profile_data_1
    )
    assert user_profile_resp_1.status_code == 200

    user_profile_payload_1 = user_profile_resp_1.json()
    assert (user_profile_payload_1["user"].get("email") ==
            user_profile_setemail_put_data_1.get("email"))


def test_user_profile_sethandle_invalid_token(_url):
    """ this will test invalid token"""

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }
    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    user_profile_sethandle_put_data_1 = {
        "token": "invalid token",
        "handle_str": "ValidHandle",
    }
    user_profile_sethandle_resp_1 = requests.put(
        _url + "/user/profile/sethandle", json=user_profile_sethandle_put_data_1
    )
    assert user_profile_sethandle_resp_1.status_code == InputError.code


def test_user_profile_sethandle_invalid_handle(_url):
    """ this will test invalid handle"""

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }
    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_sethandle_put_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "handle_str": "",
    }
    user_profile_sethandle_resp_1 = requests.put(
        _url + "/user/profile/sethandle", json=user_profile_sethandle_put_data_1
    )
    assert user_profile_sethandle_resp_1.status_code == InputError.code


def test_user_profile_sethandle_used_handle(_url):
    """ this will test used_handle"""

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }
    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200
    auth_register_payload_1 = auth_register_resp_1.json()

    # create another user for preparing for a used handle
    auth_register_post_data_2 = {
        'email': 'simple2@email.com',
        'password': '12345678sdf',
        'name_first': 'Ming',
        'name_last': 'Kai',
    }

    auth_register_resp_2 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_2
    )
    assert auth_register_resp_2.status_code == 200
    auth_register_payload_2 = auth_register_resp_2.json()

    user_profile_get_data_1 = {
        "token": auth_register_payload_2.get("token"),
        "u_id": auth_register_payload_2.get("u_id"),
    }
    user_profile_resp_1 = requests.get(
        _url + "/user/profile", params=user_profile_get_data_1
    )
    assert user_profile_resp_1.status_code == 200
    user_profile_payload_1 = user_profile_resp_1.json()

    user_profile_sethandle_put_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "handle_str": user_profile_payload_1["user"].get("handle_str"),
    }
    user_profile_sethandle_resp_1 = requests.put(
        _url + "/user/profile/sethandle", json=user_profile_sethandle_put_data_1
    )
    assert user_profile_sethandle_resp_1.status_code == InputError.code


def test_user_profile_sethandle_correct(_url):
    """ this will test whether user_profile_sethandle can work or not"""

    clear_url = _url + "/clear"
    clear_resp = requests.delete(clear_url)
    assert clear_resp.status_code == 200

    auth_register_post_data_1 = {
        'email': 'simple@email.com',
        'password': '12345678sdf',
        'name_first': 'Xing',
        'name_last': 'Shi',
    }
    auth_register_resp_1 = requests.post(
        _url + "/auth/register", json=auth_register_post_data_1
    )
    assert auth_register_resp_1.status_code == 200

    auth_register_payload_1 = auth_register_resp_1.json()

    user_profile_sethandle_put_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "handle_str": "ValidHandle",
    }
    user_profile_sethandle_resp_1 = requests.put(
        _url + "/user/profile/sethandle", json=user_profile_sethandle_put_data_1
    )
    assert user_profile_sethandle_resp_1.status_code == 200

    user_profile_data_1 = {
        "token": auth_register_payload_1.get("token"),
        "u_id": auth_register_payload_1.get("u_id"),
    }
    user_profile_resp_1 = requests.get(
        _url + "/user/profile", params=user_profile_data_1
    )
    assert user_profile_resp_1.status_code == 200

    user_profile_payload_1 = user_profile_resp_1.json()
    assert (user_profile_payload_1["user"].get("handle_str") ==
            user_profile_sethandle_put_data_1.get("handle_str"))
