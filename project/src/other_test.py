# -*- coding: utf-8 -*-
""" Implementation for testing other.py """

import time
import pytest

from auth import auth_register
from channel import channel_join, channel_messages
from channel import channel_addowner, channel_details, channel_invite
from channels import channels_create
from user import user_profile
from message import message_send
from other import clear, users_all, admin_userpermission_change, search
from other import admin_user_remove
from error import InputError, AccessError


def test_clear():
    """Test for the correct implementation for clear function"""
    clear()
    auth_register("simple@example.org", "123456", "sh", "LA")
    clear()
    auth_register("simple@example.org", "123456", "sh", "LA")


def test_user_all():
    """Test for the correct implementation for user_all function"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Stark")
    user1 = user_profile(reg1["token"], reg1["u_id"])
    user2 = user_profile(reg1["token"], reg2["u_id"])

    assert(users_all(reg1["token"]) == {
        "users": [
            user1["user"],
            user2["user"]
        ]
    })

    # Extra test for is a new user return in user_all
    reg3 = auth_register("simple@mail.com", "easyPass", "Shin", "On")
    user3 = user_profile(reg1["token"], reg3["u_id"])
    assert(users_all(reg1["token"]) == {
        "users": [
            user1["user"],
            user2["user"],
            user3["user"]
        ]
    })


def test_invalid_token_user_all():
    """Test for user_all(AccessError) invalid token"""
    with pytest.raises(AccessError):
        users_all("SomeToken")


def test_adimin_user_remove():
    clear()
    user_1 = auth_register("simple@example.com", "123456", "Hayden", "Jacobs")

    with pytest.raises(InputError):
        admin_user_remove(user_1.get("token"), -1)

    user_2 = auth_register("simple@example.org", "123456", "Ian", "Thorvaldson")

    with pytest.raises(AccessError):
        admin_user_remove(user_2.get("token"), user_1.get("u_id"))
    
    channels_create(user_1.get("token"), "COMP1531_Hayden", True)
    channel_2 = channels_create(user_2.get("token"), "COMP1531_Ian", True)

    channel_invite(user_2.get("token"), channel_2.get("channel_id"), user_1.get("u_id"))

    admin_user_remove(user_1.get("token"), user_2.get("u_id"))

    detail_dict = channel_details(user_1.get("token"), channel_2.get("channel_id"))

    assert not user_2.get("token") in detail_dict.get("owner_members")
    assert not user_2.get("token") in detail_dict.get("all_members") 

        

def test_admin_userpermission_change():
    """Test for the correct implementation for admin_userpermission_change"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Stark")
    reg3 = auth_register("simple@mail.com", "easyPass", "Shin", "On")

    info = channels_create(reg3["token"], "1531", False)

    admin_userpermission_change(reg1["token"], reg2["u_id"], 1)
    channel_join(reg1["token"], info["channel_id"])


def test_invalid_user_id_admin_userpermission_change():
    """test for invalid user_id(InputError) for admin_userpermission_change"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")

    with pytest.raises(InputError):
        admin_userpermission_change(reg1["token"], 132, 1)


def test_invalid_permission_id_admin_userpermission_change():
    """
    test for invalid permission_id(InputError)
    for admin_userpermission_change
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Stark")

    with pytest.raises(InputError):
        admin_userpermission_change(reg1["token"], reg2["u_id"], 5)


def test_user_is_not_global_owner_admin_userpermission_change():
    """
    test for user is not a global owner(AccessError)
    for admin_userpermission_change
    """
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple2@gamil.com", "123456", "Tony", "Stark")

    with pytest.raises(AccessError):
        admin_userpermission_change(reg2["token"], reg1["u_id"], 2)


def test_search():
    """Test for the correct implementation for search"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    reg2 = auth_register("simple22@example.com", "123456", "Tony", "Stark")
    reg3 = auth_register("simple@mail.com", "easyPass", "Shin", "On")

    info = channels_create(reg1["token"], "1531", True)
    channel_join(reg3["token"], info["channel_id"])

    message = "Today is a good day to go to beach!"
    info_mes = message_send(reg1["token"], info["channel_id"], message)
    info_mes2 = message_send(reg3["token"], info["channel_id"], "???")
    info_mes3 = message_send(reg1["token"], info["channel_id"], "I dont know")
    info_mes4 = message_send(
        reg3["token"], info["channel_id"], "beach is fun!")

    search_dict = search(reg1["token"], "beach")
    u_list = list(map(lambda x: x["message_id"], search_dict["messages"]))
    assert info_mes["message_id"] in u_list
    assert info_mes2["message_id"] not in u_list
    assert info_mes3["message_id"] not in u_list
    assert info_mes4["message_id"] in u_list

    # test when the user has no channel
    search_dict = search(reg2["token"], "beach")
    assert search_dict["messages"] == []


def test_search_empty_str():
    """Test for searching an empty query_str(InputError) for search"""
    clear()
    reg1 = auth_register("simple@example.org", "123456", "sh", "LA")
    with pytest.raises(InputError):
        search(reg1["token"], "")


def test_invalid_token_search():
    """Test for search(AccessError) invalid token"""
    with pytest.raises(AccessError):
        search("some_token", "beach")

