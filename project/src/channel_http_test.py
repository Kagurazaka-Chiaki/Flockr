# -*- coding: utf-8 -*-
""" Tests for channel.py in flask """

import re
import json
import signal
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

######################### Test for channel_invite ##############################


def test_valid_channel_invite(_url):
    """A function that test channel_invite valid for http"""
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_invite = requests.post(f"{_url}/channel/invite", json={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": info2["u_id"]
    })
    assert ch_invite.status_code == 200
    ch_invite = ch_invite.json()

    channel_dict = requests.get(f"{_url}/channel/details", params={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"]
    })
    assert channel_dict.status_code == 200
    channel_dict = channel_dict.json()

    user_list = list(
        map(lambda x: x.get("u_id"), channel_dict.get("all_members"))
    )
    assert info2["u_id"] in user_list


def test_channel_invite_invalid_channel_id(_url):
    """
    A testing for http invite function:
        it create two users and one invite another within a wrong channel id
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_invite = requests.post(f"{_url}/channel/invite", json={
        "token": info1["token"],
        "channel_id": 100,
        "u_id": info2["u_id"]
    }).json()
    assert ch_invite["code"] == InputError.code


def test_channel_invite_invalid_user(_url):
    """
    A testing for http function:
        where it create two users and one invite another within a wrong user id
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    wrong = info1["u_id"] + 1
    ch_invite = requests.post(f"{_url}/channel/invite", json={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": wrong
    }).json()

    assert ch_invite["code"] == InputError.code


def test_invalid_member(_url):
    """
    A testing for http invite function:
        it create two users and one invite another within a wrong token
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_invite = requests.post(f"{_url}/channel/invite", json={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": info2["u_id"]
    }).json()
    assert ch_invite["code"] == AccessError.code


######################### Test for channel_details #############################


def test_valid_channel_details(_url):
    """
    test the correct condition for http function channel_details
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_detail = requests.get(f"{_url}/channel/details", params={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"]
    })
    assert ch_detail.status_code == 200
    ch_detail = ch_detail.json()

    assert ch_detail["all_members"] == [
        {
            'u_id': info1["u_id"],
            'name_first': "Tony",
            'name_last': "Stark",
            "profile_img_url": ""
        }
    ]
    assert ch_detail["name"] == "Comp1531"


def test_channel_details_invalid_channel_id(_url):
    """
    test the error conditions (invalid channel_id) for
    http function channel_details
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_detail = requests.get(f"{_url}/channel/details", params={
        "token": info1["token"],
        "channel_id": 22
    })
    ch_detail = ch_detail.json()

    assert ch_detail["code"] == InputError.code


def test_channel_details_not_a_member(_url):
    """
    Test the error conditions (not a member) for
    http function channel_details
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_detail = requests.get(f"{_url}/channel/details", params={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"]
    })
    ch_detail = ch_detail.json()

    assert ch_detail["code"] == InputError.code


######################### Test for channel_messages ############################


def test_valid_channel_messages(_url):
    """
    Test the correct conditions for http function channel_messages
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    i = 0
    while i < 20:
        requests.post(f"{_url}/message/send", json={
            "token": info1["token"],
            "channel_id": ch_create["channel_id"],
            "message": "all"
        })
        i = i + 1

    dict_messages = requests.get(f"{_url}/channel/messages", params={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
        "start": 1
    })
    dict_messages = dict_messages.json()

    for i in dict_messages["messages"]:
        assert i["message"] == "all"

    assert dict_messages["end"] == -1

    i = 0
    while i < 35:
        requests.post(f"{_url}/message/send", json={
            "token": info1["token"],
            "channel_id": ch_create["channel_id"],
            "message": "For the future"
        })
        i = i + 1

    dict_messages = requests.get(f"{_url}/channel/messages", params={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
        "start": 0
    })
    dict_messages = dict_messages.json()

    assert dict_messages["end"] == 50


def test_channel_messages_invalid_channel_id(_url):
    """
    Test the error conditions(invalid channel_id)
    for http function channel_messages
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    dict_messages = requests.get(f"{_url}/channel/messages", params={
        "token": info1["token"],
        "channel_id": 22,
        "start": 0
    })
    dict_messages = dict_messages.json()

    assert dict_messages["code"] == InputError.code


def test_channel_messages_invalid_member(_url):
    """
    Test the error conditions(not a member in channel)
    for http function channel_messages
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    dict_messages = requests.get(f"{_url}/channel/messages", params={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"],
        "start": 0
    })
    dict_messages = dict_messages.json()

    assert dict_messages["code"] == InputError.code


def test_channel_messages_invalid_start(_url):
    """
    Test the error conditions(invalid start)
    for http function channel_messages
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    dict_messages = requests.get(f"{_url}/channel/messages", params={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
        "start": 3
    })
    dict_messages = dict_messages.json()

    assert dict_messages["code"] == InputError.code


######################### Test for channel_leave ###############################


def test_channel_valid_leave(_url):
    """
    Test the correct conditions for http function channel_leave
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_leave = requests.post(f"{_url}/channel/leave", json={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
    })
    assert ch_leave.status_code == 200
    ch_leave = ch_leave.json()

    ch_list = requests.get(f"{_url}/channels/list", params={
        "token": info1["token"]
    })
    assert ch_list.status_code == 200
    ch_list = ch_list.json()

    assert ch_list["channels"] == []


def test_channel_leave_invalid_channel_id(_url):
    """
    Test the error conditions(invalid channel_id)
    for http function channel_leave
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_leave = requests.post(f"{_url}/channel/leave", json={
        "token": info1["token"],
        "channel_id": 22,
    })
    ch_leave = ch_leave.json()

    assert ch_leave["code"] == InputError.code


def test_channel_leave_not_member(_url):
    """
    Test the error conditions(not a member)
    for http function channel_leave
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_leave = requests.post(f"{_url}/channel/leave", json={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"],
    })
    ch_leave = ch_leave.json()

    assert ch_leave["code"] == InputError.code


########################## Test for channel_join ###############################


def test_valid_channel_join(_url):
    """
    Test the correct conditions for http function channel_join
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_join = requests.post(f"{_url}/channel/join", json={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"],
    })
    assert ch_join.status_code == 200
    ch_join = ch_join.json()

    ch_list = requests.get(f"{_url}/channels/list", params={
        "token": info2["token"]
    })
    assert ch_list.status_code == 200
    ch_list = ch_list.json()

    assert ch_list["channels"] == [
        {
            "channel_id": ch_create["channel_id"],
            "name": "Comp1531"
        }
    ]


def test_channel_join_invalid_channel_id(_url):
    """
    Test the error conditions(invalid channel_id)
    for http function channel_join
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_join = requests.post(f"{_url}/channel/join", json={
        "token": info1["token"],
        "channel_id": 22,
    })
    ch_join = ch_join.json()

    assert ch_join["code"] == InputError.code


def test_channel_join_not_public_channel(_url):
    """
    Test the error conditions(user try to join a not public channel)
    for http function channel_join
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": False
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_join = requests.post(f"{_url}/channel/join", json={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"],
    })
    ch_join = ch_join.json()

    assert ch_join["code"] == AccessError.code


######################### Test for channel_addowner ############################


def test_channel_valid_addowner(_url):
    """
    Test the correct conditions for http function channel_addowner
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_add = requests.post(f"{_url}/channel/addowner", json={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": info2["u_id"]
    })
    assert ch_add.status_code == 200
    ch_add = ch_add.json()

    assert ch_add == {}


def test_channel_addowner_invalid_channel_id(_url):
    """
    Test the error conditions(invalid channel_id)
    for http function channel_addowner
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_add = requests.post(f"{_url}/channel/addowner", json={
        "token": info1["token"],
        "channel_id": 22,
        "u_id": info1["u_id"]
    })
    ch_add = ch_add.json()

    assert ch_add["code"] == InputError.code


def test_channel_addowner_already_an_owner(_url):
    """
    Test the error conditions(already an owner in channel)
    for http function channel_addowner
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_add = requests.post(f"{_url}/channel/addowner", json={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": info1["u_id"]
    })
    ch_add = ch_add.json()

    assert ch_add["code"] == InputError.code


def test_channel_addowner_not_authorised(_url):
    """
    Test the error conditions(user is not authorised)
    for http function channel_addowner
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_add = requests.post(f"{_url}/channel/addowner", json={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": info1["u_id"]
    })
    ch_add = ch_add.json()

    assert ch_add["code"] == AccessError.code


####################### Test for channel_removeowner ###########################


def test_channel_valid_removeowner(_url):
    """
    Test the correct conditions for http function channel_removeowner
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_add = requests.post(f"{_url}/channel/addowner", json={
        "token": info1["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": info2["u_id"]
    })
    assert ch_add.status_code == 200

    ch_remove = requests.post(f"{_url}/channel/removeowner", json={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": info1["u_id"]
    })
    assert ch_remove.status_code == 200
    ch_remove = ch_remove.json()

    assert ch_remove == {}


def test_channel_removeowner_invalid_channel_id(_url):
    """
    Test the error conditions(invalid channel_id)
    for http function channel_removeowner
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    ch_remove = requests.post(f"{_url}/channel/removeowner", json={
        "token": info1["token"],
        "channel_id": 22,
        "u_id": info1["u_id"]
    })
    ch_remove = ch_remove.json()

    assert ch_remove["code"] == InputError.code


def test_channel_removeowner_not_an_owner(_url):
    """
    Test the error conditions(user is not an owner)
    for http function channel_removeowner
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_remove = requests.post(f"{_url}/channel/removeowner", json={
        "token": info1["token"],
        "channel_id": 22,
        "u_id": info2["u_id"]
    })
    ch_remove = ch_remove.json()

    assert ch_remove["code"] == InputError.code


def test_channel_removeowner_not_authorised(_url):
    """
    Test the error conditions(user is not authorised)
    for http function channel_removeowner
    """
    requests.delete(f"{_url}/clear")

    info1 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2@gamil.com",
        "password": "123456",
        "name_first": "Tony",
        "name_last": "Stark"
    })
    info1 = info1.json()

    info2 = requests.post(f"{_url}/auth/register", json={
        "email": "simple2000@hotmail.com",
        "password": "123456",
        "name_first": "Simple",
        "name_last": "Name"
    })
    info2 = info2.json()

    ch_create = requests.post(f"{_url}/channels/create", json={
        "token": info1["token"],
        "name": "Comp1531",
        "is_public": True
    })
    assert ch_create.status_code == 200
    ch_create = ch_create.json()

    ch_remove = requests.post(f"{_url}/channel/removeowner", json={
        "token": info2["token"],
        "channel_id": ch_create["channel_id"],
        "u_id": info1["u_id"]
    })
    ch_remove = ch_remove.json()

    assert ch_remove["code"] == AccessError.code
