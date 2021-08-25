# -*- coding: utf-8 -*-
""" Implementation for channel.py """

import util as u
from error import InputError, AccessError
from data import Data


def channel_invite(token, channel_id, u_id):
    """
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately

    Args:
        token: (string) identfy user
        channel_id: (string) channel's id
        u_id: (interger) invited uesr id

    Returns:
        A dict containing users_token
        For example: ['Hayden_Jacobs#1', 'Ian_Thorvaldson#2']

    Raises:
        InputError("Invalid Channel"): channel_id does not refer to a valid channel.
        InputError("Invalid User"): u_id does not refer to a valid user
        AccessError("Not a Member"): the authorised user is not already a member of the channel
    """

    if not u.is_channel_id_valid(channel_id):
        raise InputError("Invalid Channel")
    if not u.is_user_id_valid(u_id):
        raise InputError("Invalid User")
    if not u.is_member(token, channel_id):
        raise AccessError("Not a Member")
    if u.is_already_a_member(u_id, channel_id):
        raise AccessError("User already a member")

    channel_dict = u.get_channel_dict(channel_id)
    channel_dict["users_token"].append(u.get_token(u_id))

    return {}


def channel_details(token, channel_id):
    """

    Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel

    Args:
        token: A string used to identify a user.
        channel_id: A integer to identify a channel.

    Returns:
        A dictionary of the channel's name , the list of owners
        and a list of members:

        {'name': name_channel,
        'owner_members': owner,
        'all_members': member,}

    Raises:
        InputError("Invalid channel"): when the channel_id is not a valid
        AccessError("You are not in this channel"):
            when the token not in the channel of channel_id

    """
    if not u.is_channel_id_valid(channel_id):
        raise InputError("Invalid channel")
    if not u.is_member(token, channel_id):
        raise AccessError("You are not in this channel")
    owner = []
    member = []
    for i in Data["channels"]:
        if i.get("channel_id") == channel_id:
            name_channel = i.get("name")
            for j in i["owners_token"]:
                dic_owner = u.get_user_detail_token(j)
                owner.append(dic_owner)
            for k in i["users_token"]:
                dic_member = u.get_user_detail_token(k)
                member.append(dic_member)
    return {
        'name': name_channel,
        'owner_members': owner,
        'all_members': member,
    }


def channel_messages(token, channel_id, start):
    """

    Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50".
    Message with index 0 is the most recent message in the channel.
    This function returns a new index "end" which is the value of "start + 50",
    or, if this function has returned the least recent messages in the channel,
    returns -1 in "end" to indicate there are no more messages to load after
    this return.

    Args:
        token: A string used to identify a user.
        channel_id: A integer to identify a channel.
        start: A integer which means the start position of messages

    Returns:
        A dictionary of a list of message dictionary ,
        the start integer and end integer

        {'messages': message,
        'start': start,
        'end': end,}

    Raises:
        InputError("Invalid channel"):when the channel_id is not a valid
        AccessError("You are not in this channel"):
            when the token not in the channel of channel_id
        InputError("Invalid start"):
            when the start is larger than total messages


    """
    if not u.is_channel_id_valid(channel_id):
        raise InputError("Invalid channel")
    if not u.is_member(token, channel_id):
        raise AccessError("You are not in this channel")
    if not u.check_message_total(start, channel_id):
        raise InputError("Invalid start")

    end = 0
    channel_dict = u.get_channel_dict(channel_id)
    total = len(channel_dict["channel_message"])
    if (start + 50) >= total:
        end = -1
    else:
        end = start + 50
    message = []
    all_message = channel_dict.get("channel_message")
    if end == -1:
        for j in range(start, total):
            message_temp = all_message[total - j - 1]
            reacts = []
            new_reacts_dict = {}
            new_reacts_dict["react_id"] = 1
            for i in message_temp["reacts"]:
                if i["react_id"] == 1:
                    new_reacts_dict["u_ids"] = i["u_ids"]
                    u_id = u.get_uid(token)

                    if u_id in i["u_ids"]:
                        new_reacts_dict["is_this_user_reacted"] = True
                    else:
                        new_reacts_dict["is_this_user_reacted"] = False
                    reacts.append(new_reacts_dict)
                    message_result = {}

            message_result = {
                "message_id": message_temp["message_id"],
                "u_id": message_temp["u_id"],
                "is_pinned":message_temp["is_pinned"],
                "reacts": reacts,
                "message": message_temp["message"],
                "time_created":message_temp["time_created"],
            }

            message.append(message_result)
    else:
        for j in range(start, end):
            message_temp = all_message[total - j - 1]
            reacts = []
            new_reacts_dict = {}
            new_reacts_dict["react_id"] = 1
            for i in message_temp["reacts"]:
                if i["react_id"] == 1:
                    new_reacts_dict["u_ids"] = i["u_ids"]
                    u_id = u.get_uid(token)

                    if u_id in i["u_ids"]:
                        new_reacts_dict["is_this_user_reacted"] = True
                    else:
                        new_reacts_dict["is_this_user_reacted"] = False
                    reacts.append(new_reacts_dict)
                    message_result = {}

            message_result = {
                "message_id": message_temp["message_id"],
                "u_id": message_temp["u_id"],
                "is_pinned":message_temp["is_pinned"],
                "reacts": reacts,
                "message": message_temp["message"],
                "time_created":message_temp["time_created"],
            }

            message.append(message_result)
    return {
        'messages': message,
        'start': start,
        'end': end,
    }


def channel_leave(token, channel_id):
    """
    Given a channel ID, the user removed as a member of this channel

    Args:
        token: A string identify user
        channel_id: An integer identify a channel

    Raises:
        InputError("nonexistent Channel ID"): when the channel_id is not valid
        AccessError("You are not in this channel"): when the user is not in the channel
    """

    if not u.is_channel_id_valid(channel_id):
        raise InputError("nonexistent Channel ID")
    if not u.is_member(token, channel_id):
        raise AccessError("You are not in this channel")

    for channel in Data["channels"]:
        if channel["channel_id"] == channel_id:
            channel["users_token"].remove(token)
            if token in channel["owners_token"]:
                channel["owners_token"].remove(token)

    return {}


def channel_join(token, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join, adds them to that channel

    Args:
        token: A string identify user
        channel_id: An integer identify a channel

    Raises:
        InputError("nonexistent Channel ID"): when the channel_id is not valid
        AccessError("This channel is private"): when the channel is private and
        the user is not a global owner
    """
    if not u.is_channel_id_valid(channel_id):
        raise InputError("nonexistent Channel ID")
    if (not u.is_channel_public(channel_id)
            and not u.is_global_owner(token)):
        raise AccessError("This channel is private")

    for channel in Data["channels"]:
        if channel["channel_id"] == channel_id:
            channel['users_token'].append(token)

    return {}


def channel_addowner(token, channel_id, u_id):
    """
    This function allows an owner of this channel
    to add an another user to be owner with their user id
    Args:
        token: A string used to identify a owner
        channel_id: An integer used to identify a channel
        u_id: A string used to identify a user
    returns:
        An empty dictionary
    Raises:
        InputError("Invalid channel_id"): when the channel_id is invalid
        InputError("User is not an owner"): when the user is an owner
        AccessError("Authorised user is not an owner"):
        when the authorised user is not an owner
    """
    if not u.is_channel_id_valid(channel_id):
        raise InputError("Invalid channel_id")
    if u.is_user_an_owner(channel_id, u_id):
        raise InputError("User is already an owner")
    if not u.is_authorised(token, channel_id):
        raise AccessError("Authorised user is not an owner")
    user_token = u.get_token(u_id)
    for channel in Data["channels"]:
        if channel.get("channel_id") == channel_id:
            channel["owners_token"].append(user_token)

    return {}


def channel_removeowner(token, channel_id, u_id):
    """
    This function allows an owner of this channel
    to remove an user's owner with their user id
    Args:
        token: A string used to identify a owner
        channel_id: An integer used to identify a channel
        u_id: A string used to identify a user
    returns:
        An empty dictionary
    Raises:
        InputError("Invalid channel_id"): when the channel_id is invalid
        InputError("User is not an owner"): when the user is not an owner
        AccessError("Authorised user is not an owner"):
        when the authorised user is not an owner
    """
    if not u.is_channel_id_valid(channel_id):
        raise InputError("Invalid channel_id")
    if not u.is_user_an_owner(channel_id, u_id):
        raise InputError("User is not an owner")
    if not u.is_authorised(token, channel_id):
        raise AccessError("Authorised user is not an owner")
    user_token = u.get_token(u_id)
    for channel in Data["channels"]:
        if channel.get("channel_id") == channel_id:
            channel["owners_token"].remove(user_token)

    return {}
