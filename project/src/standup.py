# -*- coding: utf-8 -*-
""" Implementation for standup.py """

from datetime import timezone, datetime, timedelta
from data import Data
from error import InputError, AccessError
import util as u
from threading import Timer
from message import message_send


def standup_start(token, channel_id, length):
    """
    A function that start a standup in the channel for X seconds
    Args:
        token: A string used to identify the user
        channel_id: An integer identify a channel
        length: An integer that tell how long does the standup last
    Return:
        The time that standup end
        {
            "time_finish": 1,
        }
    Raise:
        InputError("Channel not exist")
            when the channel_id does not belong to a channel
        InputError("Standup is currently running in this channel")
            when standup is already active
        AccessError("You are not in this channel")
            when the authorised user is not in the channel
    """
    if not u.is_channel_exist(channel_id):
        raise InputError("Channel not exist")
    if u.is_standup_running(channel_id):
        raise InputError("Standup is currently running in this channel")
    if not u.is_member(token, channel_id):
        raise AccessError("You are not in this channel")

    channel_dict = u.get_channel_dict(channel_id)
    now = datetime.now(timezone.utc)
    new_time = now + timedelta(seconds=length)
    new_time = int(new_time.timestamp())

    channel_dict["is_active"] = True
    channel_dict["time_finish"] = new_time

    send_later = Timer(length, do_standup_send, (token, channel_id))
    send_later.start()

    return {
        "time_finish": new_time
    }

def standup_active(token, channel_id):
    """
    A function that return whether a standup is active in the channel, and
    what times does the standup end.
    Args:
        token: A string used to identify the user
        channel_id: An integer identify a channel
    Return:
        the boolen of is_active and
        The time that standup end
        {
            "is_active": False or True,
            "time_finish": 1,
        }
    Raise:
        InputError("Channel not exist")
            when the channel_id does not belong to a channel
        AccessError("Invalid token")
            when the token does not belong to a user
    """
    if not u.is_channel_exist(channel_id):
        raise InputError("Channel not exist")
    if not u.is_token_valid(token):
        raise AccessError("Invalid token")

    standup_dict = {}
    channel_dict = u.get_channel_dict(channel_id)

    if not channel_dict["is_active"]:
        standup_dict = {
            "is_active": channel_dict["is_active"],
            "time_finish": None,
        }
    else:
        standup_dict = {
            "is_active": channel_dict["is_active"],
            "time_finish": channel_dict["time_finish"],
        }
    return standup_dict

def standup_send(token, channel_id, message):
    """
    A function that store the message and user token to a list named
    standup_buffer when the standup is active in the given channel
    Args:
        token: A string used to identify the user
        channel_id: An integer identify a channel
        message: A string that user want to send to channel
    Return:
        return an empty dictionary
    Raise:
        InputError("Channel not exist")
            when the channel_id does not belong to a channel
        InputError("Message is too long")
            when the message is too long
        InputError("Standup is currently not running in this channel")
            when the standup is not active in this channel
        AccessError("You are not in this channel")
            when the authorised user is not in the channel
    """
    if not u.is_channel_exist(channel_id):
        raise InputError("Channel not exist")
    if len(message) > 1000:
        raise InputError("Message is too long")
    if not u.is_standup_running(channel_id):
        raise InputError("Standup is currently not running in this channel")
    if not u.is_member(token, channel_id):
        raise AccessError("You are not in this channel")

    channel_dict = u.get_channel_dict(channel_id)
    standup_dict = {
        "token": token,
        "message": message,
    }
    channel_dict["standup_buffer"].append(standup_dict)

    return {}

def do_standup_send(token, channel_id):
    """
    A helper function that send all the message in the standup buffer to
    the channel
    """
    channel_dict = u.get_channel_dict(channel_id)
    channel_dict["is_active"] = False
    channel_dict["time_finish"] = None
    if len(channel_dict["standup_buffer"]) != 0:
        standup_message = []
        for i in channel_dict["standup_buffer"]:
            user_dict = u.get_users_dict(i["token"])
            message = user_dict["handle_str"] + ": " + i["message"]
            standup_message.append(message)
        message = '\n'.join(standup_message)
        channel_dict["standup_buffer"] = []
        message_send(token, channel_id, message)