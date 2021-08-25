# -*- coding: utf-8 -*-
""" HTTP tests for other.py """
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


def test_other_users_all_invalid_token(_url):
    """
    test invalid token condition for users_all
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_one = user_one.json()
    new_token = info_one.get("token") + "a"

    data_two = requests.get(f"{_url}/users/all", params={"token": new_token})

    info_two = data_two.json()

    assert info_two.get("code") == AccessError.code
    # assert info_two.get("message") == "<p>Invalid token</p>"


def test_other_users_all_correct(_url):
    """
    test correct condition for users_all
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
    new_id = info_one.get("u_id")
    user_two = requests.post(f"{_url}/auth/register", json={
        "email": "dfslyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_two = user_two.json()
    info_two.get("token")

    data_three = requests.get(f"{_url}/users/all", params={"token": new_token})

    info_three = data_three.json()

    data_four = requests.get(f"{_url}/user/profile", params={"token": new_token,
                                                             "u_id": new_id})
    info_four = data_four.json()
    new_dict = info_four["user"]
    new_handle = new_dict.get("handle_str")
    user_dict = {
        'u_id': info_one.get("u_id"),
        'email': "lyuhaotian@gmail.com",
        'name_first': "Haotian",
        'name_last': "Lyu",
        'handle_str': new_handle,
        "profile_img_url": ""
    }

    assert user_dict in info_three["users"]
    assert len(info_three["users"]) == 2


def test_other_admin_invalid_permission(_url):
    """
    test invalid permission id condition for admin/userpermission/change
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
    new_id = info_one.get("u_id")

    data_two = requests.post(
        f"{_url}/admin/userpermission/change",
        json={
            "token": new_token,
            "u_id": new_id,
            "permission_id": 3,
        }
    )

    info_two = data_two.json()

    assert info_two.get("code") == InputError.code
    # assert info_two.get("message") == "<p>Invalid permission_id</p>"


def test_other_admin_invalid_uid(_url):
    """
    test invalid u_id condition for admin/userpermission/change
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
    new_id = info_one.get("u_id") + 1

    data_two = requests.post(f"{_url}/admin/userpermission/change",
                             json={"token": new_token,
                                   "u_id": new_id,
                                   "permission_id": 1, })

    info_two = data_two.json()

    assert info_two.get("code") == InputError.code
    # assert info_two.get("message") == "<p>Invalid User</p>"


def test_other_admin_invalid_token(_url):
    """
    test not global token condition for admin/userpermission/change
    """
    requests.delete(f"{_url}/clear")
    requests.post(f"{_url}/auth/register", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })

    user_two = requests.post(f"{_url}/auth/register", json={
        "email": "dfslyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_two = user_two.json()
    token_two = info_two.get("token")
    id_two = info_two.get("u_id")

    data_three = requests.post(f"{_url}/admin/userpermission/change",
                               json={"token": token_two,
                                     "u_id": id_two,
                                     "permission_id": 1, })

    info_three = data_three.json()

    assert info_three.get("code") == AccessError.code
    # assert info_three.get("message") == "<p>Authorised user is not global owner</p>"


def test_other_admin_correct(_url):
    """
    test correct condition for admin/userpermission/change
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
    new_id = info_one.get("u_id")

    user_two = requests.post(f"{_url}/auth/register", json={
        "email": "dfslyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_two = user_two.json()
    token_two = info_two.get("token")
    id_two = info_two.get("u_id")

    data_three = requests.post(f"{_url}/admin/userpermission/change",
                               json={"token": new_token,
                                     "u_id": id_two,
                                     "permission_id": 1, })

    info_three = data_three.json()
    data_four = requests.post(f"{_url}/admin/userpermission/change",
                              json={"token": token_two,
                                    "u_id": new_id,
                                    "permission_id": 1, })
    info_four = data_four.json()
    assert info_three.get("code") is None
    assert info_four.get("code") is None


def test_other_search_empty_query(_url):
    """
    test error condition of empty query for /search
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

    data_one = requests.get(f"{_url}/search", params={"token": new_token,
                                                      "query_str": ""})

    info_one = data_one.json()

    assert info_one.get("code") == InputError.code
    # assert info_one.get("message") == "<p>Can't search an empty string</p>"


def test_other_search_invalid_token(_url):
    """
    test error condition of invalid token for /search
    """
    requests.delete(f"{_url}/clear")
    user_one = requests.post(f"{_url}/auth/register", json={
        "email": "lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_one = user_one.json()
    new_token = info_one.get("token") + "a"

    data_one = requests.get(f"{_url}/search", params={"token": new_token,
                                                      "query_str": "a"})

    info_one = data_one.json()

    assert info_one.get("code") == AccessError.code
    # assert info_one.get("message") == "<p>Invalid token</p>"


def test_other_search_correct(_url):
    """
    test correct condition for /search
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

    data_two = requests.post(f"{_url}/channels/create", json={
        "token": new_token,
        "name": "test channel",
        "is_public": True,
    })

    info_two = data_two.json()
    channel_id = info_two.get("channel_id")

    requests.post(f"{_url}/message/send", json={
        "token": new_token,
        "channel_id": channel_id,
        "message": "I love cats"
    })

    requests.post(f"{_url}/message/send", json={
        "token": new_token,
        "channel_id": channel_id,
        "message": "I hate cats"
    })

    requests.post(f"{_url}/message/send", json={
        "token": new_token,
        "channel_id": channel_id,
        "message": "I love dogs"
    })

    data_three = requests.get(f"{_url}/search", params={"token": new_token,
                                                        "query_str": "cat"})

    info_three = data_three.json()

    assert len(info_three["messages"]) == 2


def test_other_clear(_url):
    '''
    test the clear function
    '''
    requests.delete(f"{_url}/clear")
    requests.post(f"{_url}/auth/register", json={
        "email": "2lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })

    requests.delete(f"{_url}/clear")
    data_two = requests.post(f"{_url}/auth/register", json={
        "email": "2lyuhaotian@gmail.com",
        "password": "lyuhaotian2001",
        "name_first": "Haotian",
        "name_last": "Lyu",
    })
    info_two = data_two.json()

    assert info_two.get("u_id") == 1

