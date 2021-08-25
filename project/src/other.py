# -*- coding: utf-8 -*-
""" Implementation for other.py """

from data import Data
from error import InputError, AccessError
import util as u


def clear():
    """
    Resets the internal data of the application to it's initial state
    """

    Data["users"].clear()
    Data["channels"].clear()


def users_all(token):
    """
    This function will returns a list of all users and their associated details
    Args:
        token: A string used to identify a user
    Returns:
        A list of all users and their associated details
        {
            'users': [
                {
                    'u_id': 1,
                    'email': 'cs1531@cse.unsw.edu.au',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'hjacobs',
                },
            ],
        }
    Raises:
        AccessError("Invalid token")
            when the token does not belong to a user
    """

    # test the validation of the token
    if not u.is_token_valid(token):
        raise AccessError("Invalid token")

    # u_id, email, name_first, name_last, handle_str, profile_img_url
    all_users = []

    for i in Data["users"]:
        user_dict = {
            "u_id": i.get("u_id"),
            "email": i.get("email"),
            "name_first": i.get("name_first"),
            "name_last": i.get("name_last"),
            "handle_str": i.get("handle_str"),
            "profile_img_url": i.get("profile_img_url"),
        }
        all_users.append(user_dict)

    return {
        'users': all_users
    }

def admin_user_remove(token, u_id):
    """
    Given a User by their user ID, remove the user from the flock.

    Args:
        token: A string used to identify the authorised user
        u_id: An integer used to identify an user
    Raises:
        InputError("Invalid User")
            when:u_id does not refer to a valid user
        AccessError("Authorised user is not global owner")
            when The authorised user is not an owner of the flock.
    """

    if not u.is_user_id_valid(u_id):
        raise InputError("Invalid User")
    if not u.is_global_owner(token):
        raise AccessError("Authorised user is not global owner")

    removed_token = u.get_token(u_id)

    Data["users"].remove(u.get_users_dict(removed_token))

    for i in Data["channels"]:
        if removed_token in i.get("owners_token"):
            i["owners_token"].remove(removed_token)
        if removed_token in i.get("users_token"):
            i["users_token"].remove(removed_token)
    
    return {}




def admin_userpermission_change(token, u_id, permission_id):
    """
    A function set the user permissions to
    a new permissions described by permission_id
    Args:
        token: A string used to identify the authorised user
        u_id: An integer used to identify an user
        permission_id: An integer used to identify their global permissions
    Raises:
        InputError("Invalid User")
            when u_id dont belong to an user
        InputError("Invalid permission_id")
            when permisson_id was no valid
        AccessError("Authorised user is not global owner")
            when the given user's token is not a global owner
    """

    if not u.is_user_id_valid(u_id):
        raise InputError("Invalid User")
    if not u.is_permission_id_valid(permission_id):
        raise InputError("Invalid permission_id")
    if not u.is_global_owner(token):
        raise AccessError("Authorised user is not global owner")

    for user in Data["users"]:
        if user["u_id"] == u_id:
            user["permission_id"] = permission_id
    return {}


def search(token, query_str):
    """
    A function that return a collection of messages that contained the query
    string in all of the channels that the user has joined
    Args:
        token: A string used to identify the user
        query_str: The string that the user is searching for
    Return:
        A list of message and its detail
        {
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
        }
    Raise:
        InputError("Can't search an empty string")
            when the query_str is empty
        AccessError("Invalid token")
            when the token does not belong to a user
    """

    all_message = []
    if u.is_query_str_empty(query_str):
        raise InputError("Can't search an empty string")
    if not u.is_token_valid(token):
        raise AccessError("Invalid token")

    for channel in Data["channels"]:
        if u.is_member(token, channel["channel_id"]):
            for i in channel["channel_message"]:
                if not i["message"].find(query_str) == -1:
                    message_dict = {
                        'message_id': i["message_id"],
                        'u_id': i["u_id"],
                        'message': i["message"],
                        'time_created': i["time_created"]
                    }
                    all_message.append(message_dict)

    return {
        'messages': all_message
    }
