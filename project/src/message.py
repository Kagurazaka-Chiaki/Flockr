# -*- coding: utf-8 -*-
""" Implementation for message.py """

import util as u
from util import TimerThread
from error import InputError, AccessError
from data import Data


def message_send(token, channel_id, message):
    """
    Send a message from authorised_user to the channel specified by channel_id

    Args:
        token: A string used to identify a user.
        channel_id: A integer to identify a channel.
        message: A string that user want to send to channel

    Returns:
        A dictionary with message's id

        {'message_id': new_id,}

    Raises:
        InputError("Message is too long"): the message input is too long
        InputError("Channel not exist"): the input channel is not exist
        AccessError("Not a Member"): the token is not the member if channel

    """
    if len(message) > 1000:
        raise InputError("Message is too long")
    if not u.is_channel_exist(channel_id):
        raise InputError("Channel not exist")
    if not u.is_member(token, channel_id):
        raise AccessError("Not a Member")

    channel_dict = u.get_channel_dict(channel_id)
    if channel_dict["channel_message"] == []:
        message_id = 1
        new_id = u.generate_message_id(channel_id, message_id)
    else:
        new_id = u.get_last_id(
            channel_dict["channel_message"], "message_id") + 1

    u_id = u.get_uid(token)

    new_time = u.unix_timestamp()

    message_dict = {
        "message_id": new_id,
        "u_id": u_id,
        "message": message,
        "time_created": new_time,
        "reacts": [],
        "is_pinned": False,
    }

    for i in Data["channels"]:
        if i.get("channel_id") == channel_id:
            i["channel_message"].append(message_dict)

    return {
        'message_id': new_id,
    }


def message_remove(token, message_id):
    """
    Given a message_id for a message, this message is removed from the channel

    Args:
        token: (string) identfy user
        message_id: (interger) message id

    Returns:
        A empty dictionary {}

    Raises:
        InputError("No Longer Exists"): Message (based on ID) no longer exists
        AccessError("Not Authorised"):
            None of Message with message_id was sent by the authorised user
            And the authorised user is an owner of this channel or the flockr
    """

    channel_id = u.get_channel_id(message_id)

    if not u.is_message_exist(message_id):
        raise InputError("No Longer Exists")

    if ((not u.is_global_owner(token)) and
        (not u.is_channel_owner(token, channel_id)) and
        (not u.is_message_owner(token, message_id))):
        raise AccessError("Not Authorised")

    message_list = u.get_message_list(channel_id)

    for i in message_list:
        if i.get("message_id") == message_id:
            message_list.remove(i)

    return {}


def message_edit(token, message_id, message):
    """
    Given a message, update it's text with new text.
    If the new message is an empty string, the message is deleted.

    Args:
        token: (string) identfy user
        message_id: (interger) message id
        message: A string that user want to send to channel

    Returns:
        A empty dictionary {}

    Raises:
        AccessError("Not Authorised"):
            None of Message with message_id was sent by the authorised user
            And the authorised user is an owner of this channel or the flockr
    """
    channel_id = u.get_channel_id(message_id)

    if ((not u.is_global_owner(token)) and
        (not u.is_channel_owner(token, channel_id)) and
        (not u.is_message_owner(token, message_id))):
        raise AccessError("Not Authorised")

    message_list = u.get_message_list(channel_id)
    for message_dic in message_list:
        if message_dic["message_id"] == message_id:
            if message == "":
                message_remove(token, message_id)
            else:
                message_dic["message"] = message

    return {
    }


def message_react(token, message_id, react_id):
    """
    Given a message within a channel the authorised user is part of,
    add a "react" to that particular message

    Args:
        token: (string) identfy user
        message_id: (interger) message id
        react_id: (interger) type of react id

    Returns:
        A empty dictionary {}

    Raises:
        InputError("Invalid react"):
            the react id is invalid
        InputError("No this message"):
            the message is not exist in this channel
        InputError("Already reacts"):
            the react of user is already exist
    """
    if not u.is_message_exist(message_id):
        raise InputError("message_id is not a valid")
    if not u.is_react_id_valid(react_id):
        raise InputError("react_id is no valid")
    if u.is_already_react(token, message_id, react_id):
        raise InputError("already reacted to the message")

    channel_id = u.get_channel_id(message_id)
    message_list = u.get_message_list(channel_id)

    authorised_user_id = u.get_uid(token)
    for i in message_list:
        if i.get("message_id") == message_id:
            react_list = i.get("reacts")

            if react_list == []:
                new_react_dict = {
                    "react_id": react_id,
                    "u_ids":[authorised_user_id],
                }
                react_list.append(new_react_dict)
            else:
                for react in react_list:
                    if react_id == react["react_id"]:
                        react["u_ids"].append(authorised_user_id)

    return {

    }


def message_unreact(token, message_id, react_id):
    """
    Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message

    Args:
        token: (string) identfy user
        message_id: (interger) message id
        react_id: (interger) type of react id

    Returns:
        A empty dictionary {}

    Raises:
        InputError("Invalid react"):
            the react id is invalid
        InputError("No this message"):
            the message is not exist in this channel
        InputError("Already reacts"):
            the react of user is not exist
    """
    if not u.is_message_exist(message_id):
        raise InputError("message_id is not a valid")
    if not u.is_react_id_valid(react_id):
        raise InputError("react_id is no valid")
    if not u.is_already_react(token, message_id, react_id):
        raise InputError("have not reacted to the message")

    channel_id = u.get_channel_id(message_id)
    message_list = u.get_message_list(channel_id)

    authorised_user_id = u.get_uid(token)
    for i in message_list:
        if i.get("message_id") == message_id:
            react_list = i.get("reacts")
            for react in react_list:
                if react_id == react["react_id"]:
                    react["u_ids"].remove(authorised_user_id)

    return {

    }


def message_pin(token, message_id):
    """
    Given a message within a channel, mark it as "pinned" to be
    given special display treatment by the frontend

    Args:
        token: (string) identfy user
        message_id: (interger) message id

    Returns:
        A empty dictionary {}

    Raises:
        InputError("No this message"):
            the message is not exist in this channel
        InputError("Already unpinned"):
            the message is already pinned
        AccessError("Not a member"):
            the user is not the member of this channel
        AccessError("Not a owner"):
            the user is not the owner of this channel
    """
    if not u.is_message_exist(message_id):
        raise InputError("No this message")
    if u.check_pin(message_id):
        raise InputError("Already pinned")

    current_channel_id = u.get_channel_id(message_id)

    if not u.is_member(token, current_channel_id):
        raise AccessError("Not a member")
    if not u.is_authorised(token, current_channel_id):
        raise AccessError("Not a owner")

    message_list = u.get_message_list(current_channel_id)
    for i in message_list:
        if i.get("message_id") == message_id:
            i["is_pinned"] = True

    return {
    }


def message_unpin(token, message_id):
    """
    Given a message within a channel, remove it's mark as unpinned

    Args:
        token: (string) identfy user
        message_id: (interger) message id

    Returns:
        A empty dictionary {}

    Raises:
        InputError("No this message"):
            the message is not exist in this channel
        InputError("Already unpinned"):
            the message is already unpinned
        AccessError("Not a member"):
            the user is not the member of this channel
        AccessError("Not a owner"):
            the user is not the owner of this channel
    """
    if not u.is_message_exist(message_id):
        raise InputError("No this message")
    if not u.check_pin(message_id):
        raise InputError("Already unpinned")

    current_channel_id = u.get_channel_id(message_id)

    if not u.is_member(token, current_channel_id):
        raise AccessError("Not a member")
    if not u.is_authorised(token, current_channel_id):
        raise AccessError("Not a owner")

    message_list = u.get_message_list(current_channel_id)
    for i in message_list:
        if i.get("message_id") == message_id:
            i["is_pinned"] = False

    return {
    }


def message_sendlater(token, channel_id, message, time_sent):
    interval = time_sent - u.unix_timestamp()

    if interval < 0:
        raise InputError("Invalid Time")
    
    # if is_past_time(time_sent):
    #     raise InputError("Past Time")

    if len(message) > 1000:
        raise InputError("Message is too long")
    if not u.is_channel_exist(channel_id):
        raise InputError("Channel not exist")
    if not u.is_member(token, channel_id):
        raise AccessError("Not a Member")

    later = TimerThread(interval, message_send, (token, channel_id, message))
    later.run()
    return later.result()