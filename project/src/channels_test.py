# -*- coding: utf-8 -*-
""" Tests for channels.py """

import pytest

from other import clear
from error import InputError, AccessError
from auth import auth_register
from channel import channel_join
from channels import channels_list, channels_create, channels_listall


def test_invalid_name():
    """ create a name longer than 20 and check whether is valid """
    clear()
    with pytest.raises(InputError):
        channels_create("Hayden_Jacobs#1", "COMP1531____________20", True)


def test_invalid_token():
    """ create a user check with a wrong token """
    clear()
    auth_register("simple@example.com", "123456", "Hayden", "Jacobs")
    with pytest.raises(AccessError):
        channels_create("Ian_Thorvaldson#2", "COMP1531", True)


def test_valid_channel():
    """ create two users and two channels and check whether info equal """
    clear()
    user1 = auth_register("simple@example.edu", "123456", "Hayden", "Jacobs")
    primary_info = channels_create(user1.get("token"), "COMP1531", True)
    auth_register("simple@example.org", "123456", "Ian", "Thorvaldson")
    second_info = channels_create(user1.get("token"), "COMP1531", True)
    assert primary_info != second_info


def test_channels_list_invalid_token():
    """ test the error situation of the channles_list function"""
    with pytest.raises(AccessError):
        channels_list('invalid_token')


def test_channels_list():
    """ test whether channels_list can work correctly or not"""
    # call auth_register to create two users and use info to store their information
    info_one = auth_register("validemailtom@ins.com",
                             'password', "Tom", "David")
    channel_id_one = channels_create(info_one['token'], "channel_one", True)
    info_two = auth_register("validemailjulia@ins.com",
                             "password", "Kai", "Julia")
    channel_id_two = channels_create(info_two['token'], "channel_two", True)

    # we move the first user into the channel_two
    channel_join(info_one['token'], channel_id_two["channel_id"])

    result = channels_list(info_one['token'])

    for index, channel in enumerate(result['channels']):
        if index == 0:
            assert channel['channel_id'] == channel_id_one['channel_id']
            assert channel['name'] == "channel_one"
        elif index == 1:
            assert channel['channel_id'] == channel_id_two['channel_id']
            assert channel['name'] == "channel_two"

    clear()


def test_channels_list_all_invalid_token():
    """ test the error situation of the channles_listall function"""
    with pytest.raises(AccessError):
        channels_listall('invalid_token')


def test_channels_list_all():
    """ test whether channels_listall can work correctly or not"""
    info_one = auth_register("validemailtom@ins.com",
                             'password', "Tom", "David")
    channel_id_one = channels_create(info_one['token'], "channel_one", True)
    info_two = auth_register("validemailjulia@ins.com",
                             "password", "Kai", "Julia")
    channel_id_two = channels_create(info_two['token'], "channel_two", True)
    info_three = auth_register(
        "validemailvivian@ins.com", 'password', "Mei", "Vivian")
    channel_id_three = channels_create(
        info_three['token'], "channel_three", False)

    result = channels_listall(info_one['token'])

    for index, channel in enumerate(result['channels']):
        if index == 0:
            assert channel['channel_id'] == channel_id_one['channel_id']
            assert channel['name'] == "channel_one"
        elif index == 1:
            assert channel['channel_id'] == channel_id_two['channel_id']
            assert channel['name'] == "channel_two"
        elif index == 2:
            assert channel['channel_id'] == channel_id_three['channel_id']
            assert channel['name'] == "channel_three"

    clear()
