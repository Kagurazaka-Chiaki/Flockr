# -*- coding: utf-8 -*-
""" Public methods collection and helper functions """
from email.utils import parseaddr, formataddr
from email.header import Header
import re
import threading
from threading import Event
# import datetime as dt
from datetime import timezone, datetime
from data import Data


################################ General tool ##################################

def get_last_id(datalist, itemname):
    """ return the last user id """
    try:
        temp = datalist.pop()
    except IndexError:
        return 0
    else:
        newid = temp.get(itemname)
        datalist.append(temp)
    return newid


def is_token_valid(token):
    """
    Check wether is token valid
    return trun if valid
    """
    for i in Data["users"]:
        if i.get("token") == token:
            return True
    return False

################################# For auth.py #################################


def is_email_valid(email):
    """
    Email entered is not a valid email
    return true if vaild
    """
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    return not bool(re.match(regex, email) is None)


def is_email_used(email):
    """
    Email address is already being used by another user
    Email entered does belong to a user
    return true if used
    """
    for i in Data["users"]:
        if i.get("email") == email:
            return True
    return False


def is_password_short(password):
    """
    Password entered is less than 6 characters long
    return true if short
    """
    return bool(len(password) < 6)


def is_name_in_range(first, last):
    """
    first name and last name not is between 1 and 50 characters in length
    return true if in range
    """
    return bool(((len(first) in range(1, 51)) and len(last) in range(1, 51)))


def generate_permission_id(itemname):
    """
    Generate a permission_id for new user.
    All users are members by default
    except the first user will be global owner
    """
    return 1 if len(itemname) == 0 else 2

def format_addr(info):
    """
    formate the message
    """
    name, addr = parseaddr(info)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def check_reset_code(reset_code):
    """ check the reset code from the user"""
    for user in Data["users"]:
        if user["reset_code"] == reset_code:
            return True
    return False

def get_info_from_reset(reset_code):
    """ get infomation from reset_code"""
    for user in Data["users"]:
        if user["reset_code"] == reset_code:
            return user
    return None
################################ For channel.py ################################


def is_user_id_valid(u_id):
    """
    Check whether is valid user_id
    return true if valid
    """
    for i in Data["users"]:
        if i.get("u_id") == u_id:
            return True
    return False


def is_channel_id_valid(channel_id):
    """
    Check whether is valid channel_id
    return true if vaild
    """
    for i in Data["channels"]:
        if i.get("channel_id") == channel_id:
            return True
    return False


def get_channel_dict(channel_id):
    """ return a dict contains specific channels by channel_id """
    channel_dict = {}
    for i in Data["channels"]:
        if i.get("channel_id") == channel_id:
            channel_dict = i
    return channel_dict


def is_channel_public(channel_id):
    """
    Check whether is the public channel
    return true if it is punlic
    """
    result = False
    for channel in Data["channels"]:
        if channel["channel_id"] == channel_id:
            result = bool(channel["is_public"])
    return result


def get_token(uid):
    """ return a specific token by u_id """
    token = ""
    for i in Data["users"]:
        if i.get("u_id") == uid:
            token = i["token"]
    return token


def is_member(token, channel_id):
    """
    Check whether the user is a member in channel
    return true if is member
    """
    channel_dict = get_channel_dict(channel_id)
    return bool(token in channel_dict["users_token"])


def check_message_total(start, channel_id):
    """ check total message """
    check = True
    total = 0
    for i in Data["channels"]:
        if i.get("channel_id") == channel_id:
            total = len(i["channel_message"])
            if start > total:
                check = False
    return bool(check)


def get_user_detail_token(token):
    """ return a dict contains user's detail by token """
    temp = {}
    for i in Data["users"]:
        if i.get("token") == token:
            temp = {
                "u_id": i["u_id"],
                "name_first": i["name_first"],
                "name_last": i["name_last"],
                "profile_img_url": i["profile_img_url"],
            }
    return temp


def is_user_an_owner(channel_id, u_id):
    """
    Check wether the user is one of the channel owner
    return true if it is owner
    """
    user_token = get_token(u_id)
    channel_dict = get_channel_dict(channel_id)
    return bool(user_token in channel_dict["owners_token"])


def is_authorised(token, channel_id):
    """
    Check wether the user is authorised
    return true if it is owner
    """
    channel_dict = get_channel_dict(channel_id)
    return bool(token in channel_dict["owners_token"])


def is_already_a_member(u_id, channel_id):
    """ Check invited user is already a member """
    user_token = get_token(u_id)
    channel_dict = get_channel_dict(channel_id)
    return user_token in channel_dict.get("users_token")

################################ For channels.py ###############################


def is_name_valid(name):
    """
    Check the name is not valid for its length greater than 20
    return true if valid
    """
    return bool(len(name) < 20)


################################ For message.py  ###############################


def get_uid(token):
    """ return a specific u_id by token """
    u_id = 0
    for i in Data["users"]:
        if i.get("token") == token:
            u_id = i["u_id"]
    return u_id


def is_channel_exist(channel_id):
    '''
    Check channel exist or not
    return true if exist
    '''
    return not bool(get_channel_dict(channel_id) == {})


def generate_message_id(channel_id, message_id):
    '''generate the message id'''
    return (channel_id << 32) | message_id


def get_channel_id(message_id):
    ''' get channel id from message id'''
    return message_id >> 32


def unix_timestamp():
    """ return current unix time stamp """
    time = datetime.now(timezone.utc)
    return int(time.timestamp())


def get_message_list(channel_id):
    """ Return the message list """
    channel_dict = get_channel_dict(channel_id)
    return channel_dict.get("channel_message")


def is_message_exist(message_id):
    """
    Check whether the message is already removed
    return true if exist
    """
    message_list = get_message_list(get_channel_id(message_id))
    for i in message_list:
        if i.get("message_id") == message_id:
            return True
    return False


def is_global_owner(token):
    """
    Check whether the user is the global owner
    return true if is global owner
    """
    for i in Data["users"]:
        if (i.get("token") == token and i.get("permission_id") == 1):
            return True
    return False


def is_channel_owner(token, channel_id):
    """
    Check whether the user is the owner of the channel
    return true if is channel owner
    """
    channel_dict = get_channel_dict(channel_id)
    if token in channel_dict.get("owners_token"):
        return True
    return False


def is_message_owner(token, message_id):
    """
    Check whether the user is the owner of the message
    return true if is message owner
    """
    channel_id = get_channel_id(message_id)
    message_list = get_message_list(channel_id)

    u_id = get_uid(token)

    for i in message_list:
        if i.get("message_id") == message_id:
            if i.get("u_id") == u_id:
                return True
    return False


def get_users_dict(token):
    """ return a dict contains specific user's information """
    users_dict = {}
    for i in Data["users"]:
        if i.get("token") == token:
            users_dict = i
    return users_dict


################################ For user.py ##################################


def is_handle_in_range(handle):
    """
    test whether the handle is valid in length or not
    Args:
        handle: the string needs to be tested
    Returns:
        True: handle is valid in length
        False: handle is invalid in length
    """
    return bool((len(handle) in range(3, 21)))


def is_handle_str_used(handle):
    """
    find out the handle is used by other people or not
    Args:
        handle: the string needs to be tested
    Returns:
        True: handle is used by others
        False: handle is not used
    """
    for i in Data["users"]:
        if i.get("handle_str") == handle:
            return True
    return False


################################ For other.py ##################################


def is_permission_id_valid(permission_id):
    """
    Check is the permission id valid
    return ture if permission is 1 or 2
    """
    return bool(permission_id in (1, 2))


def is_query_str_empty(query_str):
    """
    Check the query string is empty
    return ture if is empty
    """
    return bool(len(query_str) == 0)

def is_standup_running(channel_id):
    """ A helper function that check is the standup active """
    channel_dict = get_channel_dict(channel_id)
    return channel_dict["is_active"]



########################## For message in iteration 3 ##########################


def is_already_react(token, message_id, react_id):
    """test if the user has already reacted to the message"""
    channel_id = get_channel_id(message_id)
    message_list = get_message_list(channel_id)

    authorised_user_id = get_uid(token)
    for i in message_list:
        if i.get("message_id") == message_id:
            react_list = i["reacts"]
            for react in react_list:
                if react_id == react["react_id"]:
                    if authorised_user_id in react["u_ids"]:
                        return True
    return False


def is_react_id_valid(react_id):
    """test if the react_id is valid"""
    return bool(react_id == 1)


def check_pin(message_id):
    """help function to check pinned or not"""
    message_list = get_message_list(get_channel_id(message_id))
    for i in message_list:
        if i.get("message_id") == message_id:
            if i["is_pinned"]:
                return True
    return False


def is_image_in_range(img, x_start, y_start, x_end, y_end):
    """ Check whether if the coordinates is in range of image size """
    start_range = bool(x_start >= 0 and y_start >= 0)
    end_range = bool(x_end <= img.size[0] and y_end <= img.size[1])
    print(img.size, start_range, end_range)
    return bool(start_range and end_range)

# The code below is based on the TimerThread in the module threading.py,
# we define a result function which return the self value.
class TimerThread(threading.Thread):
    """Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=None, kwargs=None)
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """
    def __init__(self, interval, function, args=None, kwargs=None):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()
        self.value = None

    # def cancel(self):
    #     """Stop the timer if it hasn't finished yet."""
    #     self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.value = self.function(*self.args, **self.kwargs)
        self.finished.set()

    def result(self):
        """ return the self value """
        return self.value

# def is_past_time(time_sent):
#     """test if the send time is in the past"""
#     current_time = dt.datetime.utcnow()
#     timestamp = current_time.replace(tzinfo=dt.timezone.utc).timestamp()
#     return bool((time_sent - timestamp) < 0)
