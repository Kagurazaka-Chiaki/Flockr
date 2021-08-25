# -*- coding: utf-8 -*-
""" Implementation for testing other.py """

import time
import pytest

from auth import auth_register
from channel import channel_join, channel_messages
from channels import channels_create
from user import user_profile
from message import message_send
from standup import standup_start, standup_active, standup_send
from error import InputError, AccessError
from other import clear

def test_valid_standup_start():
    """Test for valid standup_start"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    info = channels_create(reg1["token"], "1531", True)

    standup_start(reg1["token"], info["channel_id"], 1)
    standup_info = standup_active(reg1["token"], info["channel_id"])

    assert standup_info["is_active"]

def test_invalid_channel_id_standup_start():
    """Test for standup_start(InputError) invalid channel_id"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    with pytest.raises(InputError):
        standup_start(reg1["token"], 2, 30)

def test_running_standup_start():
    """Test for standup_start(InputError) standup is already running"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    info = channels_create(reg1["token"], "1531", True)

    standup_start(reg1["token"], info["channel_id"], 1)
    with pytest.raises(InputError):
        standup_start(reg1["token"], info["channel_id"], 30)

def test_not_a_member_standup_start():
    """Test for standup_start(AccessError) standup is not a member"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Stark")
    info = channels_create(reg1["token"], "1531", True)

    with pytest.raises(AccessError):
        standup_start(reg2["token"], info["channel_id"], 30)

def test_valid_standup_active():
    """Test for valid standup_active"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    info = channels_create(reg1["token"], "1531", True)
    # test for standup not running
    standup_info = standup_active(reg1["token"], info["channel_id"])

    assert not standup_info["is_active"]
    assert standup_info["time_finish"] is None

    # test for standup running
    start_info = standup_start(reg1["token"], info["channel_id"], 1)
    standup_info = standup_active(reg1["token"], info["channel_id"])

    assert standup_info["is_active"]
    assert standup_info["time_finish"] == start_info["time_finish"]


def test_invalid_channel_id_standup_active():
    """Test for standup_active(InputError) Invalid channel_id"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    with pytest.raises(InputError):
        standup_active(reg1["token"], 2)

def test_invalid_token_standup_active():
    """Test for standup_active(AccessError) Invalid token"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    info = channels_create(reg1["token"], "1531", True)
    with pytest.raises(AccessError):
        standup_active("some_token", info["channel_id"])

def test_valid_standup_send():
    """Test for valid standup_send"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Stark")
    info = channels_create(reg1["token"], "1531", True)
    channel_join(reg2["token"], info["channel_id"])
    standup_start(reg1["token"], info["channel_id"], 5)
    standup_active(reg1["token"], info["channel_id"])

    standup_send(reg1["token"], info["channel_id"], "Hello")
    standup_send(reg2["token"], info["channel_id"], "Hi")
    standup_send(reg2["token"], info["channel_id"], "How are you?")
    standup_send(reg1["token"], info["channel_id"], "Thank you")
    time.sleep(5)

    standup_info = standup_active(reg2["token"], info["channel_id"])
    assert not standup_info["is_active"]
    assert standup_info["time_finish"] is None

    mess_info = channel_messages(reg1["token"], info["channel_id"], 0)
    assert len(mess_info["messages"]) == 1

def test_invalid_channel_id_standup_send():
    """Test for standup_send(InputError) Invalid channel_id"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    with pytest.raises(InputError):
        standup_send(reg1["token"], 2, "message")

def test_invalid_message_standup_send():
    """Test for standup_send(InputError) invalid message length"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    info = channels_create(reg1["token"], "1531", True)
    standup_start(reg1["token"], info["channel_id"], 1)
    message = "hello" * 1000
    with pytest.raises(InputError):
        standup_send(reg1["token"], info["channel_id"], message)

def test_not_active_standup_send():
    """Test for standup_send(InputError) standup is not active"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    info = channels_create(reg1["token"], "1531", True)
    with pytest.raises(InputError):
        standup_send(reg1["token"], info["channel_id"], "message")

def test_not_a_member_standup_send():
    """Test for standup_send(AccessError) user is not a member"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Stark")
    info = channels_create(reg1["token"], "1531", True)
    standup_start(reg1["token"], info["channel_id"], 1)
    with pytest.raises(AccessError):
        standup_send(reg2["token"], info["channel_id"], "message")
