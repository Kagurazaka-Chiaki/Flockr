# -*- coding: utf-8 -*-
"""Implementation for channels.py"""

from error import InputError, AccessError
from data import Data
import util as u


def channels_list(token):
    """
    Provide a list of all channels (and their associated details)
    that the authorised user is part of

    Args:
        token: (string) identfy authorised user

    Returns:
        A dict containing 'channels' which has the value of list of the channles
        that consists of 'channle_id' and 'channle_name'

    Raises:
        AccessError("Invalid Token"): when is not the authorised user
    """
    # test the validation of the token
    if not u.is_token_valid(token):
        raise AccessError("Invalid token")

    channel_list = []
    # need to check which channel token is part of
    for channel in Data["channels"]:
        if token in channel["users_token"]:
            new_channel = {
                'channel_id': channel['channel_id'],
                'name': channel['name']
            }
            channel_list.append(new_channel)

    return {
        'channels': channel_list
    }


def channels_listall(token):
    """
    Provide a list of all channels (and their associated details)

    Args:
        token: (string) identfy authorised user

    Returns:
        A dict containing 'channels' which has the value of list of the channels
        that consists of 'channle_id' and 'channle_name'

    Raises:
        AccessError("Invalid Token"): when is not the authorised user
    """
    # test the validation of the token
    if not u.is_token_valid(token):
        raise AccessError("Invalid token")

    all_channels = []
    for channel in Data["channels"]:
        new_channel = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        all_channels.append(new_channel)
    return {
        'channels': all_channels
    }


def channels_create(token, name, is_public):
    """
    Creates a new channel with that name
    that is either a public or private channel

    Args:
        token: (string) identfy user
        name: (stfing) channel's name
        is_public: (boolean) whether public

    Returns:
        A dict containing channel_id
        For example: {"channel_id": 1}

    Raises:
        InputError("Invalid Name"): Name is more than 20 characters long
        AccessError("Invalid Token"): when is not the authorised user
    """

    if not u.is_name_valid(name):
        raise InputError("Invalid Name")
    if not u.is_token_valid(token):
        raise AccessError("Invalid Token")

    new_channel_id = u.get_last_id(Data["channels"], "channel_id") + 1
    owners_token_list = [token]
    users_token_list = [token]

    detail = {
        "channel_id": new_channel_id,
        "name": name,
        "owners_token": owners_token_list,
        "users_token": users_token_list,
        "channel_message": [],
        "is_public": is_public,
        "standup_buffer": [],
        "is_active": False,
    }

    Data["channels"].append(detail)

    return {
        'channel_id': new_channel_id,
    }
